import os
import unittest

# if not "CONFIG_PATH" in os.environ:
#     os.environ["CONFIG_PATH"] = "whsongbook.config.TestingConfig"

import whsongbook
from whsongbook.__init__ import *

class FilterTests(unittest.TestCase):
    def test_display_chords(self):
        bad_chords = ["A#m", "Hsus"]
        expectation = False
        for b in bad_chords:
            test_out = display_chords(b)
            self.assertEqual(expectation, test_out)

if __name__ == "__main__":
    unittest.main()
