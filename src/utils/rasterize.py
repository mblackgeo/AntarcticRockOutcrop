import os
import fiona
import rasterio as rio
from rasterio import features
import rasterio.mask
import numpy as np


"""
Creates a binary raster. 1s represent pixels intersecting with the input shape. 0s represent
pixels disjoint from the input shape.
"""
def rasterize_label(raster_path, vector_path):
    with fiona.open(vector_path) as vectors:
        shapes = [features['geometry'] for features in vectors]

    with rio.open(raster_path) as base:
        meta = base.meta.copy()
        output = (rasterio.mask.mask(base, shapes, crop=True, indexes=1)[0] > 0).astype(rio.uint8)
        output = np.expand_dims(output, axis=0)
    return output, meta

"""
This function saves a raster to file

@param np array (1 * N * M) layer: single band np array to be written to file
@param rasterio meta object meta: the metadata including transform information for the layer
@param string name: The path to write the file to. extension .TIF

@returns void
"""

def save_raster(layer, meta, name):
    meta['dtype'] = layer.dtype
    meta['count'] = 1
    with rio.open(name, 'w', **meta) as dst:
        dst.write(layer)

    
