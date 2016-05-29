import os
import unittest

# if not "CONFIG_PATH" in os.environ:
#     os.environ["CONFIG_PATH"] = "whsongbook.config.TestingConfig"

import whsongbook
from whsongbook.parse import *

class Tests(unittest.TestCase):

    def test_bad_section_name(self):
        bad_section_name = """
chors:
    [f]Down on the [c]corner, [gout in the [c]street
    Willy and the [f]Poorboys are [c]playin' """

        whsongbook.parse.parse_text("BadSectionName", bad_section_name)
        self.assertTrue("BadSectionName" in whsongbook.failing_songs)

    def test_unmatched_bracket_content(self):
        unmatched_bracket_content = """
chorus:
    [f]Down on the [c]corner, [gout in the [c]street
    Willy and the [f]Poorboys are [c]playin' """

        whsongbook.parse.parse_text("UnmatchedBracketContent", unmatched_bracket_content)
        self.assertTrue("UnmatchedBracketContent" in whsongbook.failing_songs)

    def test_unmatched_bracket_header(self):
        unmatched_bracket_header = """
header:
  title = "Bare Necessities"
  artist = "Terry Gilkyson"
  year = 1967
  genres = "disney", "musical", "ragtime"]
"""
        whsongbook.parse.parse_text("UnmatchedBracketHeader", unmatched_bracket_header)
        self.assertTrue("UnmatchedBracketHeader" in whsongbook.failing_songs)

    def test_no_quotes_header(self):
        no_quotes_header = """
header:
  title = "Bare Necessities"
  artist = Terry Gilkyson
  year = 1967
  genres = ["disney", "musical", "ragtime"]
"""
        whsongbook.parse.parse_text("NoQuotesHeader", no_quotes_header)
        self.assertTrue("NoQuotesHeader" in whsongbook.failing_songs)

    def test_no_equals_header(self):
        no_equals_header = """
header:
  title = "Bare Necessities"
  artist "Terry Gilkyson"
  year = 1967
  genres = ["disney", "musical", "ragtime"]
"""
        whsongbook.parse.parse_text("NoEqualsHeader", no_equals_header)
        self.assertTrue("NoEqualsHeader" in whsongbook.failing_songs)

    def test_bad_chord(self):
        whsongbook.parse.parse_text("BadChord", """verse:
    [h]Early in the evenin' [A#5]just about supper [c]time """)
        self.assertEqual(whsongbook.failing_songs[-1], "BadChord")

    def test_check_chord(self):
        """
        Test to see if any of the chords have failed to be parsed
        """

        bad_chords = ["A#m", "Hsus"]
        expect = False
        for b in bad_chords:
            test_out = check_chord(b)
            self.assertEqual(expect, test_out)

if __name__ == "__main__":
    unittest.main()
