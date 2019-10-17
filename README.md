# Antarctic Rock Outcrop

This fork aims to remove the arcpy dependency for this script and replacing it with rasterio. This will remove the requirement of an ESRI license.
This repository contains a python script for automatically differentiating areas of rock outcrop using Landsat-8 data. The python script applies the method of Burton-Johnson, et al. (2016) to automatically identify rock outcrop areas from top of atmosphere corrected Landsat-8 tiles from Antarctica. Relevant modifications should be made for application to other Landsat datasets where band numbers may change.

## Python3 Installation
### Collect repositories
1. Clone or fork this repository
2. Clone or fork [landsat-utils](https://github.com/developmentseed/landsat-util)
### Download Scene List
3. Download supplementary material from [publication](http://dx.doi.org/10.5194/tc-2016-56) | ([Direct download link for tc-10-1665-2016-supplement.zip](https://www.the-cryosphere.net/10/1665/2016/tc-10-1665-2016-supplement.zip]))
4. Unzip supplementary material and locate "Landsat Tile IDs - Differentiating snow and rock in Antarctic.txt"
(File location in zip = "'Supplementary\ Materials'/'Landsat Tile IDs - Differentiating snow and rock in Antarctic.txt'")
5. Write a quick script to load the text file into memory (it's a tab-delimited file) and return a list of scene ids (the values in the first column). **This serves as the input for the landsat-util/landsat/downloader.py**
### Configure virtual environment
6. Create a virtual environment in your base directory

```
virtual env "env_name"
```

7. Activate your virtual environment and install pip requirements **NOTE: install requirements from this repository, not landsat-utils"**
```
source "env_name"/bin/activate
pip install -r requirements.txt
```
8. Install homura (landsat-util/landsat/downloader.py requires it). landsat-utils/requirements.txt includes versions of some packages that are no longer available.
```
pip install homura
```
You should now have everything you need to download images, correct them, and generate output from the model.

## Proof of concept usage
### Steps to create the output for a small section of a single landsat tile
This proof of concept example is designed to be run on a local machine with reasonable resources (>=4 GB memory, >= 50 GB storage)
### Download a single Landsat tile
1. Create a script that creates an instance of the landsat-util/landsat/downloader.py Downloader class.
  - The only necessary parameter is the download_dir which should be the string of a path to a directory with at least 2GB of storage. **The image correction and model scripts require that your image directory have the structure path/to/images/"SCENE_ID of a single image"/ e.g. path/to/images/LC82201072015017LGN00 that contains .tif files named "LC82201072015017LGN00_B#.TIF**
  
2. Call the Downloader.download(["scene_id"]) method on your class instance passing a list containing a single scene id from 
the Supplementary material.

### This will download a .tar.bz file into the path you specified.

3. Untar the downloaded file (This might take a while)
```
untar xf "filename"
```

You now have a directory with a .tif file for each band and a .txt file containing the correction constants.

### Convert the spectral relectance bands (1-7) to top of atmosphere reflectance and the temperature bands (10, 11) to Top of atmposphere brightness temperature.
  
4. Create an instance of the LandsatTOACorrecter class from image_correction.py
  - This class should be instantiated with the path to the directory containing the landsat tile bands.
  
5. Call the LandsatTOACorrecter.correct_toa_reflectance() method and the LandsatTOACorrecter.correct_toa_brightness_temp()

This will create a new directory "corrected" within your scene's directory with a copy of the band .tif files that have corrected values **These corrected bands are the input to the model**

### Generate the model output **NOTE: The model currently only generates output for a 512 X 512 pixel segment of the full
tile

1. Create a textfile with a single line containing the scene id (this step will be removed in future versions of the model)

2. Open the jupyter notebook burton_johnson_model.ipynb

3. In Cell 3, 
  - Change the values of landsatTileList to the name of the file created in step 1
  
  - Change the value of landsatDirectory to the directory containing the corrected bands "path/to/images/corrected/'scene id'"
  
 4. Run all cells in order except for:
  - Cell 7, first line:
  ```
  schema = {'geometry': 'Polygon', 'properties': {'area': 'float:13.3', 'id_img': 'int', 'id_ADD':'int'}}
  ```
  
  - Cells 10-14, first line of Cell 10:
  ```
with shp.Reader(coastMaskShpfile) as coast:
  ```

The final two cells write the output file to the corrected image directory and a full color image of the extent for which
the model generated. These files have suffixes "_burjo_output.tif" and "full_color_seg.tif" respectively

## Arcpy Installation

- Clone a copy of the repository, or
- [Download the latest release](https://github.com/mblack2xl/AntarcticRockOutcrop/releases/latest) 


## Arcpy Requirements

- ArcGIS >9.0
- ArcGIS Spatial Analyst Extension

## Usage

Please set the approapriate input and output directories on Lines 38-44 of this script prior to running. Top of atmosphere corrected Landsat-8 tiles can be downloaded from [USGS ESPA](https://espa.cr.usgs.gov). The first step in submitting an order for ESPA is to create a scene list. This is a simple text file (`*.txt`) listing one Landsat identifier (filename) on each line. The list can be easily generated by performing a spatial/temporal inventory search through [EarthExplorer](http://earthexplorer.usgs.gov/) and exporting search results to a spreadsheet from which filenames can be extracted. Once ESPA tiles are downloaded **ALL** tiles should be extract to the **SAME** root  directory for processing with this script. The text file of Landsat IDs required by ESPA is the same as required by this script.

The coastline mask can either be created manually or the current Antarctic coastline can be downloaded as a shapefile from the [Antarctic Digital Database](http://www.add.scar.org).

This script should be run either within ArcMap from the Python console  (Geoprocessing > Python), or from the ArcMap python command line launched from Start > Programs > ArcGIS > Python X.X > Python (command line). Once in Python, simply `execfile` using the full path to this script with escaped slashes (double backslash: `\\`), as per the example below.

To avoid any problems please ensure all files have the same geospatial referencing system and are 16-bit integer GeoTIFFs with the scaling factors as given by the [USGS ESPA Landsat 8 Product Guide](http://landsat.usgs.gov/documents/provisional_l8sr_product_guide.pdf).

## Contributing

1. Fork it
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## History

- 11 May 2016: Uploaded to GitHub
- 03 Nov 2015: Created ArcPy script

## Credits

Burton-Johnson, A., Black, M., Fretwell, P. T., and Kaluza-Gilbert, J.: A fully automated methodology for differentiating rock from snow, clouds and sea in Antarctica from Landsat imagery: A new rock outcrop map and area estimation for the entire Antarctic continent, *The Cryosphere Discuss.*, [doi:10.5194/tc-2016-56](http://dx.doi.org/10.5194/tc-2016-56), in review, 2016. 

## License

Code released under the GPLv3 license.
