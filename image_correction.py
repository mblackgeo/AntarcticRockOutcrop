"""
Class that corrects Landsat 8 OLI reflective bands to Top of Atmosphere Reflectance
and Thermal bands to Top of Atmosphere Brightness Temperature as defined
by https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level **ADD REST OF URL**

"""
import os


class LandsatTOACorrecter:


    """
    @param str scene_path: The absolute path to directory of a specific landsat scene containing
                            all bands.
    """


    def __init__(self, scene_path):
        self.path = scene_path
        self.scene_id = ""
        self.base_dir = ""
        self.mtl_path = ""
        self.configure_paths()

    def configure_paths(self):
        assert os.path.exists(self.path)
        assert os.path.isdir(self.path)
        self.scene_id = os.path.basename(self.path)
        self.base_dir = os.path.dirname(self.path)
        self.mtl_path = self.base_dir + "/" + self.scene_id + "/" + self.scene_id + "_MTL.txt"
        assert os.path.exists(self.mtl_path)



if __name__ == "__main__":
    test_img_path = "/home/dsa/DSA/images/LC82201072015017LGN00"

    test = LandsatTOACorrecter(test_img_path)
