import os
from utils.data_directory_manager import DataDirectoryManager
from landsatUtil.landsat.downloader import Downloader
from utils.image_correction import LandsatTOACorrecter
from models.antarctic_rock_outcrop_os import OutcropLabeler
from os import listdir
from os.path import isfile, join
from _thread import *
import threading 
dataPath= "data/downloads"


"""
To use script, change base_dir to the directory where you intend to store your images
"""
print_lock = threading.Lock() 


def untar_helper(threadName, scene_IDs, chunkNum, dm, totalThreads):    
    lenList = len(scene_IDs)
    chunkSize = int(lenList/totalThreads);
    start_chunk = chunkNum*chunkSize
    
    if(chunkNum + 1 == totalThreads):
        end_chunk = lenList
    else:
        end_chunk = (chunkNum+1)*chunkSize
    scene_chunk = scene_IDs[start_chunk : end_chunk ]
    for s in scene_chunk:
        print("Thread: " + threadName + " Untarring: " + s)
        dm.untar_scenes([s])
    return

if __name__ == "__main__":
    base_dir = os.getcwd()
    dm = DataDirectoryManager(os.path.join(base_dir,"data"))
    '''
    dm.download_supplement() # where we get the zip file
    dm.extract_scene_id_file() # where we get the sceneID .txt
    '''
    scene_IDs = []
    scene_IDs = [i["ID"] for i in dm.load_scene_ids()[:39]]
   
    dataFiles = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]
    fName = [i.split(".")[0].replace("'", "") for i in dataFiles] 
    for s in scene_IDs:
        if s not in fName:
            scene_IDs.remove(s)
    try:
        t1 = threading.Thread( target = untar_helper, args = ("Thread-1", scene_IDs, 0, dm, 4, ) )
        t2 = threading.Thread( target = untar_helper, args = ("Thread-2", scene_IDs, 1, dm, 4, ) )
        t3 = threading.Thread( target = untar_helper, args = ("Thread-3", scene_IDs, 2, dm, 4, ) )
        t4 = threading.Thread( target = untar_helper, args = ("Thread-4", scene_IDs, 3, dm, 4, ) )
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
    except:
       print("Error: unable to start thread")
            
            
            
#     for s in scene_IDs:
#         print("Untarring: " + s)
#         dm.untar_scenes([s])
             
    
        
#     for s in scenes:
#         scene_IDs.append(s)
#     print(scene_IDs)
#     scene_IDs_raw = os.path.join(dm.raw_image_dir, scene_IDs[0])
#     test_scene_corrected = os.path.join(dm.corrected_image_dir, scene_IDs[0])
    
    
#     print(dm.download_dir)
    
#     scene_downloader = Downloader(download_dir=dm.download_dir)
#     scene_downloader.download(scene_IDs)
#     
    
#     correcter = LandsatTOACorrecter(scene_IDs_raw)
#     correcter.correct_toa_brightness_temp(dm.corrected_image_dir)
#     correcter.correct_toa_reflectance(dm.corrected_image_dir)
    
#     labeler = OutcropLabeler(test_scene_corrected, coast_shape_file)
#     labeler.write_mask_file(dir_manager.label_dir)

#     print(test_scene)
#     print(dm.load_scene_ids())
