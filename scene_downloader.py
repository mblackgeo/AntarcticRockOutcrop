import logging
import os
import urllib.request
import zipfile

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
Given the directory in which you intend to store your landsat images, this function
downloads the supplementary material from the Burton-Johnson et. al. study (https://www.the-cryosphere.net/10/1665/2016/)
and saves the zip file to the specified directory

@:param string base_dir: absolute or relative path to the directory in which you intend to store
landsat 8 scenes. NOTE: If the directory does not exist, this function will create it!

@:returns string file_name: The absolute or relative path where the .zip file is saved
"""


def download_supplement(base_dir):
    assert base_dir is not None
    supplement_url = "https://www.the-cryosphere.net/10/1665/2016/tc-10-1665-2016-supplement.zip"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        logger.info("image directory created with path: {}".format(base_dir))

    file_name = base_dir + "/supplement.zip"

    with urllib.request.urlopen(supplement_url) as response:
        with open(file_name, 'wb') as file:
            file.write(response.read())

    logger.info("supplementary material successfully downloaded to {}".format(file_name))
    return file_name


"""
This function unzips the supplementary material zip file, moves and renames the 
text file containing the scene ids to the working directory, deleting the rest of the 
extracted directory, but preserving the source zip file

@:param string zip_path: the file path where the supplementary material zipfile is located.

@:returns string: the absolute file path to the extracted scene id text file
"""


def extract_scene_id_file(zip_path):
    assert os.path.exists(zip_path)
    base_dir = os.path.dirname(zip_path) + "/"
    scene_dir = "Supplementary Material/"
    scene_path = "Landsat Tile IDs - Differentiating snow and rock in Antarctic.txt"

    with zipfile.ZipFile(zip_path) as zf:
        zf.extract(scene_dir + scene_path, base_dir)

    logger.info("Zipfile extracted to {}".format(base_dir))

    extracted_scene_path = base_dir + "/" + scene_dir + scene_path

    clean_file_name = base_dir + "/burton_johnson_scene_ids.txt"

    os.rename(extracted_scene_path, clean_file_name)

    logger.info("Text file removed from {} and renamed to {}".format(extracted_scene_path, clean_file_name))

    for i in os.listdir(base_dir + scene_dir):
        os.remove(i)
    logger.info("all files deleted from {}".format(base_dir + scene_dir))

    os.rmdir(base_dir + scene_dir)
    logger.info("directory {} removed".format(base_dir + scene_dir))

    return clean_file_name


"""
To use script, change base_dir to the directory where you intend to store your images
"""
if __name__ == "__main__":
    base_dir = None
    test_file_name = base_dir + "/supplement.zip"
    file_name = download_supplement(base_dir)
    extract_scene_id_file(file_name)
