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
from src.utils.data_directory_manager import DataDirectoryManager

if __name__ == "__main__":
    # project_dir = os.getcwd()
    project_dir = "/home/dsa/DSA/test_project"
    dir_manager = DataDirectoryManager(project_dir)
    test_scene = [dir_manager.load_scene_ids()[0]["ID"]]

    downloader = Downloader(download_dir=dir_manager.download_dir)
    #downloader.download(test_scene)
    # this will take a while
    dir_manager.untar_scenes(test_scene)
