"""
Class that corrects Landsat 8 OLI reflective bands to Top of Atmosphere Reflectance
and Thermal bands to Top of Atmosphere Brightness Temperature as defined
by https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level **ADD REST OF URL**

"""
import os
from decimal import Decimal
import math
import numpy as np
import rasterio as rio


class LandsatTOACorrecter:

    # These values are specific to MTL.txt file provided by AWS (and maybe google too?)
    K1_PREFIX = "K1_CONSTANT_BAND_"
    K2_PREFIX = "K2_CONSTANT_BAND_"
    REFLECTANCE_MULT_PREFIX = "REFLECTANCE_MULT_BAND_"
    REFLECTANCE_ADD_PREFIX = "REFLECTANCE_ADD_BAND_"
    SUN_ELEV_PREFIX = "SUN_ELEVATION"

    """
    @param str scene_path: The absolute path to directory of a specific landsat scene containing
                            all bands.
    """

    def __init__(self, scene_path):
        self.path = scene_path
        self.scene_id = ""
        self.base_dir = ""
        self.file_prefix = ""
        self.mtl_path = ""
        self.output_dir = ""
        self.output_prefix = ""
        self.configure_paths()

        # convert dict to named tuple eventually
        self.sun_elev = 0.0
        self.refl_mult = {}
        self.refl_add = {}
        self.k1 = {}
        self.k2 = {}
        self.gather_correction_vars()

    def configure_paths(self):
        assert os.path.exists(self.path)
        assert os.path.isdir(self.path)
        self.scene_id = os.path.basename(self.path)
        self.base_dir = os.path.dirname(self.path)

        self.file_prefix = "{}/{}/{}".format(self.base_dir, self.scene_id, self.scene_id)
        self.mtl_path = self.file_prefix + "_MTL.txt"
        assert os.path.exists(self.mtl_path)

        self.output_dir = "{}/corrected/{}".format(self.base_dir, self.scene_id)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_prefix = "{}/{}".format(self.output_dir, self.scene_id)

    def gather_correction_vars(self):
        with open(self.mtl_path, 'r') as meta:
            for i in meta.readlines():
                try:
                    separator_pos = i.index(" = ")
                    key = i[:separator_pos].strip()
                    value = i[separator_pos + 3:].strip()

                    if key == self.SUN_ELEV_PREFIX:
                        self.sun_elev = value

                    if key[:len(self.REFLECTANCE_MULT_PREFIX)] == self.REFLECTANCE_MULT_PREFIX:
                        self.refl_mult[key[len(self.REFLECTANCE_MULT_PREFIX):]] = value

                    if key[:len(self.REFLECTANCE_ADD_PREFIX)] == self.REFLECTANCE_ADD_PREFIX:
                        self.refl_add[key[len(self.REFLECTANCE_ADD_PREFIX):]] = value

                    if key[:len(self.K1_PREFIX)] == self.K1_PREFIX:
                        self.k1[key[len(self.K1_PREFIX):]] = value
                    
                    if key[:len(self.K2_PREFIX)] == self.K2_PREFIX:
                        self.k2[key[len(self.K2_PREFIX):]] = value
                       
                except ValueError as e:
                    pass

    def correct_toa_reflectance(self):
        # need to load window of panchromatic bands
        self.refl_mult.pop("8")
        self.refl_add.pop("8")
        self.refl_mult.pop("9")
        self.refl_add.pop("9")
        local_solar_zenith = math.cos(math.radians(90 - float(Decimal(self.sun_elev))))

        for k, v in self.refl_mult.items():
            refl_mult_val = float(Decimal(v))
            refl_add_val = float(Decimal(self.refl_add[k]))

            band_file = self.file_prefix + "_B{}.TIF".format(k)
            output_file = self.output_prefix + "_B{}.TIF".format(k)
            assert os.path.exists(band_file)

            band, meta = self.load_band(band_file)
            meta['dtype'] = band.dtype

            corrected_band = (band * refl_mult_val + refl_add_val) / local_solar_zenith

            self.write_band(output_file, corrected_band, meta)

    def correct_toa_brightness_temp(self):
        for k, v in self.k1.items():
            k1 = float(Decimal(v))
            k2 = float(Decimal(self.k2[k]))

            band_file = self.file_prefix + "_B{}.TIF".format(k)
            output_file = self.output_prefix + "_B{}.TIF".format(k)
            assert os.path.exists(band_file)

            band, meta = self.load_band(band_file)
            meta['dtype'] = band.dtype

            corrected_band = k2 / np.log((k1 / band) + 1)

            self.write_band(output_file, corrected_band, meta)

    @staticmethod
    def load_band(path):
        with rio.open(path, 'r') as band:
            return band.read(1).astype(rio.float32), band.meta

    @staticmethod
    def write_band(path, band, meta):
        with rio.open(path, 'w', **meta) as corrected:
            corrected.write(band.astype(meta['dtype']), 1)


if __name__ == "__main__":
    test = LandsatTOACorrecter("/home/dsa/DSA/images/LC82201072015017LGN00")
    test.correct_toa_reflectance()
    test.correct_toa_brightness_temp()
