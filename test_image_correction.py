import unittest
from image_correction import LandsatTOACorrecter


class LandsatTOACorrecterTest(unittest.TestCase):
    def setUp(self) -> None:
        test_dir = "/home/dsa/DSA/images/LC82201072015017LGN00"
        test = LandsatTOACorrecter(test_dir)
