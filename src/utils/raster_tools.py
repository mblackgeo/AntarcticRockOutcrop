"""
This script has static functions used to read a window (or segment) from an entire raster tile.
"""

from itertools import product
import rasterio as rio
import rasterio.windows as wnd


def get_window(file_path, width=512, height=512, col_off=0, row_off=0):
    with rio.open(file_path) as data:
        meta = data.meta.copy()

        ncols, nrows = meta['width'], meta['height']
        offsets = product(range(0, ncols, width), range(0, nrows, height))

        full_image = wnd.Window(col_off=0, row_off=0, width=ncols, height=nrows)

        window = wnd.Window(col_off=col_off * width, row_off=row_off * height,
                            width=width, height=height).intersection(full_image)

        transform = wnd.transform(window, meta['transform'])

        meta['transform'] = transform
        meta['width'], meta['height'] = window.width, window.height

        return data.read(window=window).transpose(1, 2, 0).astype(rio.float32), meta
