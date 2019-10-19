import logging
import os
from src.utils.download_supplement_zip import download_supplement
from src.utils.extract_scene_id_file import extract_scene_id_file
from src.utils.load_scene_ids import load_scene_ids

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

    zip_file_name = download_supplement(base_dir, logger)
    scene_id_file = extract_scene_id_file(zip_file_name, logger)

    # from this list of ordered dicts, we can store the contents in a db or pass scene ids to the landsat downloader.
    scene_ids = load_scene_ids(scene_id_file)
    print(scene_ids)

