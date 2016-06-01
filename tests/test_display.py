import os
import unittest

# TODO: Determine if these two lines are necessary
# if not "CONFIG_PATH" in os.environ:
#     os.environ["CONFIG_PATH"] = "whsongbook.config.TestingConfig"

import whsongbook
from whsongbook.display import *

class DisplayTests(unittest.TestCase):

    def test_good_false_chord(self):
        good_false_chord = "(x2)"
        res = whsongbook.display.display_chord("GoodFalseChord", good_false_chord)
        self.assertEqual(res, good_false_chord)

    def test_bad_root(self):
        bad_root = {"root": "", "quality": "m"}
        whsongbook.display.display_chord("BadRoot", bad_root)
        self.assertTrue("BadRoot" in whsongbook.failing_songs)

    def test_display_good_root(self):
        good_root = {"root": "c"}
        ret = whsongbook.display.display_chord("DisplayGoodRoot", good_root)
        self.assertEqual(ret, "C")

    def test_display_good_accidental(self):
        good_accidental = {"root": "c", "accidental": "s"}
        ret = whsongbook.display.display_chord("DisplayGoodAccidental", good_accidental)
        self.assertEqual(ret, "C#")

    def test_display_good_quality(self):
        good_quality = {"root": "c", "quality": "m"}
        ret = whsongbook.display.display_chord("DisplayGoodQuality", good_quality)
        self.assertEqual(ret, "Cm")

    def test_display_good_interval(self):
        good_interval = {"root": "c", "interval": "7"}
        ret = whsongbook.display.display_chord("DisplayGoodInterval", good_interval)
        self.assertEqual(ret, "C7")

    def test_display_good_add(self):
        good_add = {"root": "c", "add": "9"}
        ret = whsongbook.display.display_chord("DisplayGoodAdd", good_add)
        self.assertEqual(ret, "Cadd9")

    def test_display_good_add_sharp(self):
        good_add_sharp = {"root": "c", "add": "9+"}
        ret = whsongbook.display.display_chord("DisplayGoodAddSharp", good_add_sharp)
        self.assertEqual(ret, "C(#9)")

    def test_display_good_add_flat(self):
        good_add_flat = {"root": "c", "quality": "m", "interval": "7", "add": "5-"}
        ret = whsongbook.display.display_chord("DisplayGoodAddFlat", good_add_flat)
        self.assertEqual(ret, "Cm7(b5)")

    def test_display_good_inversion(self):
        good_inversion = {"root": "g", "inversion": "b"}
        ret = whsongbook.display.display_chord("DisplayGoodInversion", good_inversion)
        self.assertEqual(ret, "G/B")

    def test_display_good_inversion_accidental(self):
        good_inversion_accidental = {"root": "d", "inversion": "f", "inversion_accidental": "s"}
        ret = whsongbook.display.display_chord("DisplayGoodInversionAccidental", good_inversion_accidental)
        self.assertEqual(ret, "D/F#")

if __name__ == "__main__":
    unittest.main()
