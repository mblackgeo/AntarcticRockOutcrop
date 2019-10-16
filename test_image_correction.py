import unittest
from image_correction import LandsatTOACorrecter


class LandsatTOACorrecterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_path = "/home/dsa/DSA/images/LC82201072015017LGN00"
        self.test_scene_id = "LC82201072015017LGN00"
        self.test_base_dir = "/home/dsa/DSA/images"
        self.valid_file_prefix = "/home/dsa/DSA/images/LC82201072015017LGN00/LC82201072015017LGN00"
        self.valid_mtl_path = "/home/dsa/DSA/images/LC82201072015017LGN00/LC82201072015017LGN00_MTL.txt"

        self.invalid_path = "/home/dsa/DSA/images/LC82201072015017KGN00"

    def test_configure_valid_paths_scene_id(self):
        test = LandsatTOACorrecter(self.valid_path)
        self.assertEqual(self.test_scene_id, test.scene_id)

    def test_configure_valid_paths_base_dir(self):
        test = LandsatTOACorrecter(self.valid_path)
        self.assertEqual(self.test_base_dir, test.base_dir)

    def test_configure_valid_paths_file_prefix(self):
        test = LandsatTOACorrecter(self.valid_path)
        self.assertEqual(self.valid_file_prefix, test.file_prefix)

    def test_configure_valid_paths_mtl_path(self):
        test = LandsatTOACorrecter(self.valid_path)
        self.assertEqual(self.valid_mtl_path, test.mtl_path)
