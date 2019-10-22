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
#     dm.download_supplement() # where we get the zip file
#     dm.extract_scene_id_file() # where we get the sceneID .txt
    scene_IDs = [dm.load_scene_ids()[0]["ID"]]
    scene_IDs_raw = os.path.join(dm.raw_image_dir, scene_IDs[0])
    test_scene_corrected = os.path.join(dir_manager.corrected_image_dir, test_scene[0])
    
    
    print(dm.download_dir)
#     scene_downloader = Downloader(download_dir=dm.download_dir)
#     scene_downloader.download(scene_IDs)
#     dm.untar_scenes(scene_IDs)
    correcter = LandsatTOACorrecter(scene_IDs_raw)
    correcter.correct_toa_brightness_temp(dm.corrected_image_dir)
    correcter.correct_toa_reflectance(dm.corrected_image_dir)
    
    labeler = OutcropLabeler(test_scene_corrected, coast_shape_file)
    labeler.write_mask_file(dir_manager.label_dir)

#     print(test_scene)
#     print(dm.load_scene_ids())
