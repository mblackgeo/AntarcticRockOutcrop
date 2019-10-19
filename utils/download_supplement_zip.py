import os
import urllib.request

"""
Given the directory in which you intend to store your landsat images, this function
downloads the supplementary material from the Burton-Johnson et. al. study (https://www.the-cryosphere.net/10/1665/2016/)
and saves the zip file to the specified directory

@:param string base_dir: absolute or relative path to the directory in which you intend to store
landsat 8 scenes. NOTE: If the directory does not exist, this function will create it!

@:returns string file_name: The absolute or relative path where the .zip file is saved
"""


def download_supplement(base_dir, logger):
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
