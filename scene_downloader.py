import logging
import os
import urllib.request
import zipfile

logger = logging.getLogger('scene_downloader_log')

logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('scene_download.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def download_supplement(base_dir):
    supplement_url = "https://www.the-cryosphere.net/10/1665/2016/tc-10-1665-2016-supplement.zip"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        logger.info("image directory created with path: {}".format(base_dir))

    file_name = base_dir + "/supplement.zip"

    with urllib.request.urlopen(supplement_url) as response:
        with open(file_name, 'wb') as file:
            file.write(response.read())


def extract_scene_id_file(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall()


if __name__ == "__main__":
    base_dir = "/home/dsa/DSA/image_auto"
    download_supplement(base_dir)