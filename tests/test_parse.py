import os
import unittest

# if not "CONFIG_PATH" in os.environ:
#     os.environ["CONFIG_PATH"] = "whsongbook.config.TestingConfig"

import whsongbook
from whsongbook.parse import *

class FilterTests(unittest.TestCase):
    def test_check_chord(self):
        """
        Test to see if any of the chords have failed to be parsed
        """

        bad_chords = ["A#m", "Hsus"]
        expect = False
        for b in bad_chords:
            test_out = check_chord(b)
            self.assertEqual(expect, test_out)

    def test_parse_header(self):
        """
        TODO: The function parse_header() is unused, so this test is currently useless
        """
        bad_header = """
header:
    title "I Will Follow You Into the Dark"
    artist "Death Cab for Cutie"
    capo = 5
    year = 2005
    genres = ["indie"]"""
        expect = False
        test_out = parse_header(bad_header)
        # self.assertEqual(expect, test_out)
        pass

    def test_check_section(self):
        bad_section = ["solo", ""]
        good_section = ["verse", ""]
        self.assertEqual(False, check_section(bad_section))
        self.assertEqual(True, check_section(good_section))

if __name__ == "__main__":
    unittest.main()
