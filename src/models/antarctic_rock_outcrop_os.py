#! /usr/bin/env python
"""
Rock Outcrop Identification using Landsat-8 tiles

-- Reference ---
[1] Burton-Johnson, A., Black, M., Fretwell, P. T., and Kaluza-Gilbert, J.: 
    A fully automated methodology for differentiating rock from snow, clouds
        and sea in Antarctica from Landsat imagery: A new rock outcrop map and
        area estimation for the entire Antarctic continent, The Cryosphere
        Discuss., doi:10.5194/tc-2016-56, in review, 2016.

 --- Author ---
Author: Martin Black
Email: martin.black@bas.ac.uk
Date: 2015-03-11
Version: 1.0

 --- Rewritten to remove ArcGIS and ArcPy requirement ---
 Refactorer: Sam Elkind
 Email: selkind3@gatech.edu
 Date: 2019-13-10
 Version: 0.1
"""

import sys, os, time
from itertools import product

import rasterio as rio
import rasterio.windows as wnd


class OutcropLabeler:
    COL_OFF = 11
    ROW_OFF = 13

    SUN_MASK_STEP_1_THRESHOLD = 0.4
    SUN_MASK_STEP_2_THRESHOLD = 0.70
    SUN_MASK_STEP_3_THRESHOLD = 0.45
    SUN_MASK_STEP_5_THRESHOLD = 2550.0
    SUN_MASK_FINAL_THRESHOLD = 5

    SHADE_MASK_STEP_1_THRESHOLD = 2500.0
    SHADE_MASK_STEP_2_THRESHOLD = 0.45
    SHADE_MASK_FINAL_THRESHOLD = 3

    def __init__(self, scene_path):
        self.scene_path = scene_path
        self.scene_id = os.path.basename(self.scene_path)
        self.band_prefix = os.path.join(self.scene_path, self.scene_id)
        self.b2 = None
        self.b10 = None
        self.b3 = None
        self.load_multiuse_bands()
        self.coast_mask = self.load_coast_mask()

    def get_tile(self, file, width=512, height=512, col_off=0, row_off=0):
        with rio.open(file, dtype='float32') as data:
            meta = data.meta.copy()

            ncols, nrows = meta['width'], meta['height']
            # offsets = product(range(0, ncols, width), range(0, nrows, height))
            big_window = wnd.Window(col_off=0, row_off=0, width=ncols, height=nrows)

            window = wnd.Window(col_off=col_off * width, row_off=row_off * height,
                                width=width, height=height).intersection(big_window)

            transform = wnd.transform(window, data.transform)

            meta['transform'] = transform
            meta['width'], meta['height'] = window.width, window.height

            return data.read().transpose(1, 2, 0).astype(rio.float32), meta

    # load bands with float dtypes
    # grab the band data (LANDSAT-8 OLI, bands are stacked, no Panchromatic band)
    """
    The bands loaded here are used in multiple masking layers. They are loaded here to prevent redundant io. 
    """
    def load_multiuse_bands(self):
        self.b2 = self.get_tile(self.band_prefix + "_B2.TIF", col_off=self.COL_OFF, row_off=self.ROW_OFF)  # Blue
        self.b3 = self.get_tile(self.band_prefix + "_B3.TIF", col_off=self.COL_OFF, row_off=self.ROW_OFF)  # Green
        self.b10 = self.get_tile(self.band_prefix + "_B10.TIF", col_off=self.COL_OFF, row_off=self.ROW_OFF) # TIRS1

    # TODO create coastline mask by vectorizing coast shpfile over extent of band2
    def load_coast_mask(self):
        return (self.b2[0] > 0).astype(int)

    def create_ndsi(self):
        b6 = self.get_tile(self.band_prefix + "_B6.TIF", col_off=self.COL_OFF, row_off=self.ROW_OFF)  # nir?
        ndsi = (self.b3[0] - b6[0]) / (self.b3[0] + b6[0])

        return ndsi, b6[1]

    def create_ndwi(self):
        b5 = self.get_tile(self.band_prefix + "_B5.TIF", col_off=self.COL_OFF, row_off=self.ROW_OFF)  # nir?
        ndwi = (self.b3[0] - b5[0]) / (self.b3[0] + b5[0])

        return ndwi, b5[1]

    # mask 1, sunlit rock
    def create_sun_mask(self):
        mask1_step1 = ((self.b10[0] / self.b2[0]) > self.SUN_MASK_STEP_1_THRESHOLD).astype(int)
        mask1_step2 = (self.create_ndsi()[0] < self.SUN_MASK_STEP_2_THRESHOLD).astype(int)
        mask1_step3 = (self.create_ndwi()[0] < self.SUN_MASK_STEP_3_THRESHOLD).astype(int)
        mask1_step5 = (self.b10[0] > self.SUN_MASK_STEP_5_THRESHOLD).astype(int) # note this is a scaled value
        # Calculate intersections of all sunlit masks 
        mask1_prefinal = mask1_step1 + mask1_step2 + mask1_step3 + self.coast_mask + mask1_step5

        # save pixels that intersect sunlit masks
        return (mask1_prefinal == self.SUN_MASK_FINAL_THRESHOLD).astype(int)

    # mask 2, rock in shade
    def create_shade_mask(self):
        mask2_step1 = (self.b2[0] < self.SHADE_MASK_STEP_1_THRESHOLD).astype(int) # note this is a scaled value
        mask2_step2 = (self.create_ndwi()[0] < self.SHADE_MASK_STEP_2_THRESHOLD).astype(int)
        # Calculate intersections of all shade masks
        mask2_prefinal = mask2_step1 + mask2_step2 + (1 - self.coast_mask)
        # save pixels that intersect shade masks
        return (mask2_prefinal == self.SHADE_MASK_FINAL_THRESHOLD).astype(int)

    def create_final_mask(self):
        # combine mask1 and mask2
        mask_prefinal = self.create_sun_mask() + self.create_shade_mask()
        # union of sunlight and shaded masks
        return (mask_prefinal > 0).astype(int)

    def write_mask_file(self, output_dir):
        mask = self.create_final_mask()
        meta = self.b2[1]
        meta['dtype'] = rio.uint16
        meta['width'] = mask.shape[0]
        meta['height'] = mask.shape[1]
        meta['count'] = 1
        out_file = os.path.join(output_dir, self.scene_id + "_label.TIF")

        with rio.open(out_file, 'w', **meta) as dst:
            print(dst)
            print(dst.shape)
            dst.write(mask.astype(meta['dtype']).squeeze(), meta['count'])
