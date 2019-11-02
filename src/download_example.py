import os
"""
add landsat-util submodule to system path so we can use the Downloader object
make sure the landsat-util/requirements.txt is deleted or renamed 
this is a hack to get around the dependency problems we've been having with
the landsat-util repo
"""

from landsatUtil.landsat.downloader import Downloader
from utils.data_directory_manager import DataDirectoryManager
from utils.image_correction import LandsatTOACorrecter
from models.antarctic_rock_outcrop_os import OutcropLabeler

if __name__ == "__main__":
    project_dir = os.path.join(os.getcwd(), "data")
   
    dm = DataDirectoryManager(project_dir)

    # Load a scene id from file and save it as a list with len() = 1
    scene_IDs = [dm.load_scene_ids()[0]["ID"]]
    dm.logger.info("Example scene ID: {}".format(scene_IDs))

    # Create directory name to hold raw scene bands
    test_scene_raw = os.path.join(dm.raw_image_dir, scene_IDs[0])

    # Create directory name to hold corrected scene bands
    test_scene_corrected = os.path.join(dm.corrected_image_dir, scene_IDs[0])

    # Create landsat util scene downloader
    # downloader = Downloader(download_dir=dm.download_dir)

    # downloader.download(scene_IDs)
    # this will take a while
    # dm.untar_scenes(scene_IDs)

    correcter = LandsatTOACorrecter(test_scene_raw)
    correcter.correct_toa_brightness_temp(dm.corrected_image_dir)
    correcter.correct_toa_reflectance(dm.corrected_image_dir)

    # labeler = OutcropLabeler(test_scene_corrected, dm.coast_shape_path)
    # labeler.write_mask_file(dm.label_dir)
