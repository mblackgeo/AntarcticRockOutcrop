import logging
import os
from src.utils.data_directory_manager import DataDirectoryManager

"""
To use script, change base_dir to the directory where you intend to store your images
"""
if __name__ == "__main__":
    base_dir = os.getcwd()

    pm = DataDirectoryManager(base_dir)
    pm.download_supplement()
    pm.extract_scene_id_file()

    print(pm.load_scene_ids())
