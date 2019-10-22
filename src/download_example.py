import os
# get the path to the repo directory. Might be better to use os.path.basename(sys.path[0])
code_dir = os.path.dirname(os.path.abspath(__file__))

import sys
"""
add landsat-util submodule to system path so we can use the Downloader object
make sure the landsat-util/requirements.txt is deleted or renamed 
this is a hack to get around the dependency problems we've been having with
the landsat-util repo
"""
sys.path.append(os.path.join(os.path.dirname(code_dir), "landsat-util"))

from landsat.downloader import Downloader
from utils.data_directory_manager import DataDirectoryManager
from utils.image_correction import LandsatTOACorrecter
from models.antarctic_rock_outcrop_os import OutcropLabeler

if __name__ == "__main__":
    # project_dir = os.getcwd()
    project_dir = "/home/dsa/DSA/test_project"
    coast_shape_file = "/home/dsa/DSA/vectors/Coastline_high_res_polygon_v7.1.shp"
    assert os.path.exists(coast_shape_file)
    dir_manager = DataDirectoryManager(project_dir)

    test_scene = [dir_manager.load_scene_ids()[0]["ID"]]
    test_scene_raw = os.path.join(dir_manager.raw_image_dir, test_scene[0])
    test_scene_corrected = os.path.join(dir_manager.corrected_image_dir, test_scene[0])

    # downloader = Downloader(download_dir=dir_manager.download_dir)

    #downloader.download(test_scene)
    # this will take a while
    # dir_manager.untar_scenes(test_scene)
    # correcter = LandsatTOACorrecter(test_scene_raw)
    # correcter.correct_toa_brightness_temp(dir_manager.corrected_image_dir)
    # correcter.correct_toa_reflectance(dir_manager.corrected_image_dir)

    labeler = OutcropLabeler(test_scene_corrected, coast_shape_file)
    labeler.write_mask_file(dir_manager.label_dir)
