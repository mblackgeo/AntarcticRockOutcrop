"""
Class that corrects Landsat 8 OLI reflective bands to Top of Atmosphere Reflectance
and Thermal bands to Top of Atmosphere Brightness Temperature as defined
by https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level **ADD REST OF URL**

"""
import os


class LandsatTOACorrecter:

    # These values are specific to MTL.txt file provided by AWS (and maybe google too?)
    K1_PREFIX = "K1_CONSTANT_BAND_"
    K2_PREFIX = "K2_CONSTANT_BAND_"
    REFLECTANCE_MULT_PREFIX = "REFLECTANCE_MULT_BAND_"
    REFLECTANCE_ADD_PREFIX = "REFLECTANCE_ADD_BAND_"
    SUN_ELEV_PREFIX = "SUN_ELEVATION"


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

        # convert dict to named tuple eventually
        self.refl_vars = {}
        self.k1 = {}
        self.k2 = {}
        self.refl_mult = {}
        self.refl_add = {}
        self.sun_elev = 0.0

    def configure_paths(self):
        assert os.path.exists(self.path)
        assert os.path.isdir(self.path)
        self.scene_id = os.path.basename(self.path)
        self.base_dir = os.path.dirname(self.path)
        self.mtl_path = self.base_dir + "/" + self.scene_id + "/" + self.scene_id + "_MTL.txt"
        assert os.path.exists(self.mtl_path)

    def gather_correction_vars(self):
        with open(self.mtl_path, 'r') as meta:
            for i in meta.readlines():
                print(i)



if __name__ == "__main__":
    test_img_path = "/home/dsa/DSA/images/LC82201072015017LGN00"

    test = LandsatTOACorrecter(test_img_path)
    test.gather_correction_vars()

