import os
import zipfile

"""
This function unzips the supplementary material zip file, moves and renames the 
text file containing the scene ids to the working directory, deleting the rest of the 
extracted directory, but preserving the source zip file

@:param string zip_path: the file path where the supplementary material zipfile is located.

@:returns string: the absolute file path to the extracted scene id text file
"""


def extract_scene_id_file(zip_path, logger):
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
