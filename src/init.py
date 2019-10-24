import os
from utils.data_directory_manager import DataDirectoryManager
from landsatUtil.landsat.downloader import Downloader
from utils.image_correction import LandsatTOACorrecter
from models.antarctic_rock_outcrop_os import OutcropLabeler

"""
To use script, change base_dir to the directory where you intend to store your images
"""
if __name__ == "__main__":
    base_dir = os.getcwd()
    
    dm = DataDirectoryManager(os.path.join(base_dir,"data"))

    dm.download_supplement()
    dm.extract_scene_id_file()
    
    dm.download_coast_shapefile()
    dm.extract_coast_shapefile()
