"""
Class that corrects Landsat 8 OLI reflective bands to Top of Atmosphere Reflectance
and Thermal bands to Top of Atmosphere Brightness Temperature as defined
by https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level **ADD REST OF URL**

"""
import os
import rasterio


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
        self.sun_elev = 0.0
        self.refl_mult = {}
        self.refl_add = {}
        self.k1 = {}
        self.k2 = {}
        self.gather_correction_vars()

    def configure_paths(self):
        assert os.path.exists(self.path)
        assert os.path.isdir(self.path)
        self.scene_id = os.path.basename(self.path)
        self.base_dir = os.path.dirname(self.path)
        self.file_prefix = "{}/{}/{}".format(self.base_dir, self.scene_id, self.scene_id)
        self.mtl_path = self.file_prefix + "_MTL.txt"
        assert os.path.exists(self.mtl_path)

    def gather_correction_vars(self):
        prefixex = [self.SUN_ELEV_PREFIX, self.REFLECTANCE_MULT_PREFIX, 
                    self.REFLECTANCE_ADD_PREFIX, self.K1_PREFIX, self.K2_PREFIX]

        with open(self.mtl_path, 'r') as meta:
            for i in meta.readlines():
                try:
                    separator_pos = i.index(" = ")
                    key = i[:separator_pos].strip()
                    value = i[separator_pos + 3:].strip()

                    if key == self.SUN_ELEV_PREFIX:
                       self.sun_elev = value 

                    if key[:len(self.REFLECTANCE_MULT_PREFIX)] == self.REFLECTANCE_MULT_PREFIX:
                        self.refl_mult[key[len(self.REFLECTANCE_MULT_PREFIX):]] = value

                    if key[:len(self.REFLECTANCE_ADD_PREFIX)] == self.REFLECTANCE_ADD_PREFIX:
                        self.refl_add[key[len(self.REFLECTANCE_ADD_PREFIX):]] = value

                    if key[:len(self.K1_PREFIX)] == self.K1_PREFIX:
                        self.k1[key[len(self.K1_PREFIX):]] = value
                    
                    if key[:len(self.K2_PREFIX)] == self.K2_PREFIX:
                        self.k2[key[len(self.K2_PREFIX):]] = value
                       
                except ValueError as e:
                    pass

    def correct_TOA_reflectance(self):
        for i in self.refl_mult.keys():
            band_file = self.file_prefix + "_B{}.TIF".format(i)
            assert os.path.exists(band_file)


if __name__ == "__main__":
    test_img_path = "/home/dsa/DSA/images/LC82201072015017LGN00"

    test = LandsatTOACorrecter(test_img_path)
    test.correct_TOA_reflectance()

