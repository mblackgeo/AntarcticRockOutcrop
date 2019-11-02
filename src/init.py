
import os
from utils.data_directory_manager import DataDirectoryManager
from landsatUtil.landsat.downloader import Downloader
from utils.image_correction import LandsatTOACorrecter
from utils.raster_tools import *
from models.antarctic_rock_outcrop_os import OutcropLabeler
from os import listdir
from os.path import isfile, join
from _thread import *
import threading 
import matplotlib.pyplot as plt
import rasterio.plot as rplt


import numpy as np
dataPath= "data/downloads"
rawPath = "data/raw"
stackedPath = "data/stacked_chunks"


"""
To use script, change base_dir to the directory where you intend to store your images
"""
print_lock = threading.Lock() 
un_compressed_data = []


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
        if s in un_compressed_data:
            continue
        print("Thread: " + threadName + " Untarring: " + s)
        try:
            dm.untar_scenes([s])
            print_lock.acquire()
            un_compressed_data.append(s)
            print_lock.release()
        except:
            continue
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

    #Load Already Compressed Files
    with open(rawPath+ '/raw_file.txt', 'r') as filehandle:
        for line in filehandle:
            item = line[:-1]
            un_compressed_data.append(item)
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
    #Store Compressed File 
    with open(rawPath+ '/raw_file.txt', 'w') as filehandle:
        for listitem in un_compressed_data:
            filehandle.write('%s\n' % listitem)
            
    # After Uncompressing the Images #
    rawFiles = [f for f in listdir(rawPath)]
    rawFName = [i.split(".")[0].replace("'", "") for i in rawFiles]
    
    
    
    bands = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B9", "B10", "B11"]
    for r in rawFName:
        cnt = 0;
        for b in bands:
            imgName = "data/raw/"+r + "/" + r + "_"+ b + ".TIF"
            raster = plt.imread(imgName)
            print(cnt, raster.shape)
            cnt = cnt+1
            rasters.append(raster)

        stacked_rasters = np.stack(rasters, axis=0).transpose(1,2,0)
#         print(stacked_rasters.shape)
        staked_chunks = [] 
        imgSize = stacked_rasters.shape[0]
        chunkSize = 512
        numChunks  = int(imgSize / chunkSize)
#         print(numChunks)
        cnt = 0
        dirName = stackedPath+"/"+rawFName[0] 
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        for i in range(0,numChunks):
            stIndex = i*chunkSize
            endIndex = (i+1)*chunkSize 
            chunk = stacked_rasters[stIndex:endIndex, stIndex:endIndex, :]   
            fil = np.where(chunk>0)
            nZP = np.sum(fil)
            fileName = dirName + "/chunk_" + str(i) + ".npy" 
            if(nZP > 0):
                np.save(fileName, chunk, allow_pickle = True)
                print(cnt, chunk.shape)
            cnt = cnt +1
            
         

        
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
# =======
#     data_dir = os.path.join(base_dir,"data")
#     manual_dir = "/home/dsa/DSA/images_manual"
    
#     dm = DataDirectoryManager(manual_dir)
# >>>>>>> f8f3292aab92ba89203161b3f1bdf14f78d3a094

#     dm.download_supplement()
#     dm.extract_scene_id_file()
    
#     dm.download_coast_shapefile()
#     dm.extract_coast_shapefile()
