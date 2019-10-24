import os
import logging

import urllib.request
import zipfile
import csv
import tarfile


class DataDirectoryManager:
    LOG_DIR = "logs"
    LOG_FILE = "scene_download.log"

    SUPPLEMENT_URL = "https://www.the-cryosphere.net/10/1665/2016/tc-10-1665-2016-supplement.zip"
    ZIP_NAME = "supplement.zip"

    SCENE_ID_FILE = "burton_johnson_scene_ids.txt"

    COAST_URL = "https://add.data.bas.ac.uk/repository/entry/get/Coastline_high_res_polygon_v7.1.zip?entryid=synth%3Af477219b-9121-44d6-afa6-d8552762dc45%3AL2NvYXN0bGluZXMvc2hwL0NvYXN0bGluZV9oaWdoX3Jlc19wb2x5Z29uX3Y3LjEuemlw"
    COAST_ZIP_NAME = "coastline.zip"

    COAST_DIR_NAME = "coastline"
    COAST_SHAPEFILE = "Coastline_high_res_polygon_v7.1.shp"

    RAW_IMAGES = "raw"
    CORRECTED_IMAGES = "corrected"
    OUTCROP_LABELS = "labels"
    DOWNLOADS = "downloads"

    def __init__(self, project_dir):
        self.project_dir = project_dir

        self.log_path = os.path.join(self.project_dir, self.LOG_DIR)
        self.log_file_path = os.path.join(self.log_path, self.LOG_FILE)
        self.logger = self.configure_logger()

        self.raw_image_dir = os.path.join(self.project_dir, self.RAW_IMAGES)
        self.corrected_image_dir = os.path.join(self.project_dir, self.CORRECTED_IMAGES)
        self.label_dir = os.path.join(self.project_dir, self.OUTCROP_LABELS)
        self.download_dir = os.path.join(self.project_dir, self.DOWNLOADS)
        self.coast_dir = os.path.join(self.project_dir, self.COAST_DIR_NAME)
        self.configure_data_dirs()

        self.zip_path = os.path.join(self.project_dir, self.ZIP_NAME)
        self.scene_id_file = os.path.join(self.project_dir, self.SCENE_ID_FILE)

        self.coast_zip_path = os.path.join(self.project_dir, self.COAST_ZIP_NAME)
        self.coast_shape_path = os.path.join(self.coast_dir, self.COAST_SHAPEFILE)

    def configure_logger(self):
        logger = logging.getLogger('scene_downloader_log')

        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        fh = logging.FileHandler(self.log_file_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)

        logger.addHandler(fh)

        return logger

    def configure_data_dirs(self):
        for i in [self.raw_image_dir, self.corrected_image_dir, self.label_dir, self.download_dir, self.coast_dir]:
            if not os.path.exists(i):
                os.mkdir(i)
                self.logger.info("Data directory created at {}".format(i))


    """
    Given the directory in which you intend to store your landsat images, this method
    downloads the supplementary material from the Burton-Johnson et. al. study (https://www.the-cryosphere.net/10/1665/2016/)
    and saves the zip file to the specified directory

    @:param string base_dir: absolute or relative path to the directory in which you intend to store
    landsat 8 scenes. NOTE: If the directory does not exist, this function will create it!

    @:returns string file_name: The absolute or relative path where the .zip file is saved
    """

    def download_supplement(self):
        assert self.project_dir is not None

        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
            self.logger.info("image directory created with path: {}".format(self.project_dir))

        with urllib.request.urlopen(self.SUPPLEMENT_URL) as response:
            with open(self.zip_path, 'wb') as file:
                file.write(response.read())

        self.logger.info("supplementary material successfully downloaded to {}".format(self.zip_path))

    def download_coast_shapefile(self):
        assert self.project_dir is not None

        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        with urllib.request.urlopen(self.COAST_URL) as response:
            with open(self.coast_zip_path, "wb") as file:
                file.write(response.read())

    """
    This function unzips the supplementary material zip file, moves and renames the 
    text file containing the scene ids to the working directory, deleting the rest of the 
    extracted directory, but preserving the source zip file

    @:param string zip_path: the file path where the supplementary material zipfile is located.

    @:returns string: the absolute file path to the extracted scene id text file
    """

    def extract_scene_id_file(self):
        assert os.path.exists(self.zip_path)
        scene_dir = "Supplementary Material"
        scene_file = "Landsat Tile IDs - Differentiating snow and rock in Antarctic.txt"

        with zipfile.ZipFile(self.zip_path) as zf:
            zf.extract(os.path.join(scene_dir, scene_file), self.project_dir)

        self.logger.info("Zipfile extracted to {}".format(self.project_dir))

        extracted_scene_path = os.path.join(self.project_dir, scene_dir, scene_file)

        os.rename(extracted_scene_path, os.path.join(self.project_dir, self.scene_id_file))

        self.logger.info("Text file removed from {} and renamed to {}".format(extracted_scene_path, self.scene_id_file))

        path_to_remove = os.path.join(self.project_dir, scene_dir)

        for i in os.listdir(path_to_remove):
            os.remove(i)
        self.logger.info("all files deleted from {}".format(path_to_remove))

        os.rmdir(path_to_remove)
        self.logger.info("directory {} removed".format(path_to_remove))

    def extract_coast_shapefile(self):
        assert os.path.exists(self.coast_zip_path)

        with zipfile.ZipFile(self.coast_zip_path) as zf:
            zf.extractall(self.coast_dir)

        self.logger.info("coast shapefile extracted to {}".format(self.coast_dir))

    def load_scene_ids(self):
        assert os.path.exists(self.scene_id_file)
        with open(self.scene_id_file, 'r') as tab_delim:
            reader = csv.DictReader(tab_delim, delimiter='\t')
            # list comprehension skips empty rows
            return [row for row in reader if row[list(row.keys())[0]]]

    def untar_scenes(self, scene_list):
        for i in scene_list:
            scene_tar = os.path.join(self.download_dir, i + ".tar.bz")
            assert os.path.exists(scene_tar)
            raw_scene_dir = os.path.join(self.raw_image_dir, i)
            if not os.path.exists(raw_scene_dir):
                os.mkdir(raw_scene_dir)
            with tarfile.open(scene_tar) as tar:
                tar.extractall(raw_scene_dir)
