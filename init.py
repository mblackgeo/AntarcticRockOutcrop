import logging
import os
import urllib.request
import zipfile
from utils.download_supplement_zip import download_supplement
from utils.extract_scene_id_file import extract_scene_id_file

logger = logging.getLogger('scene_downloader_log')

logger.setLevel(logging.DEBUG)

if not os.path.exists(os.getcwd() + "/logs/"):
    os.makedirs(os.getcwd() + "/logs/")

fh = logging.FileHandler(os.getcwd() + '/logs/scene_download.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


"""
To use script, change base_dir to the directory where you intend to store your images
"""
if __name__ == "__main__":
    base_dir = os.getcwd()
    test_file_name = base_dir + "/supplement.zip"
    file_name = download_supplement(base_dir, logger)
    extract_scene_id_file(file_name, logger)
