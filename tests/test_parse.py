import os
import unittest

# TODO: Determine if these two lines are necessary
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

    def test_bad_pitch_note(self):
        bad_pitch_note = "As"
        res = whsongbook.parse.parse_pitch("BadPitchNote", bad_pitch_note)
        self.assertTrue("BadPitchNote" in whsongbook.failing_songs)

    def test_bad_pitch_accidental(self):
        bad_pitch_accidental = "c#"
        res = whsongbook.parse.parse_pitch("BadPitchAccidental", bad_pitch_accidental)
        self.assertTrue("BadPitchAccidental" in whsongbook.failing_songs)

    def test_bad_pitch_duration(self):
        bad_pitch_duration = "css4"
        res = whsongbook.parse.parse_pitch("BadPitchDuration", bad_pitch_duration)
        self.assertTrue("BadPitchDuration" in whsongbook.failing_songs)

    def test_bad_pitch_extra(self):
        bad_pitch_extra = "cs4:"
        res = whsongbook.parse.parse_pitch("BadPitchExtra", bad_pitch_extra)
        self.assertTrue("BadPitchExtra" in whsongbook.failing_songs)

    def test_good_pitch(self):
        good_pitch = "bf4"
        res = whsongbook.parse.parse_pitch("GoodPitch", good_pitch)
        self.assertFalse("GoodPitch" in whsongbook.failing_songs)

    def test_bad_chord_root(self):
        bad_chord_root = "A:m"
        res = whsongbook.parse.parse_chord("BadChordRoot", bad_chord_root)
        self.assertTrue("BadChordRoot" in whsongbook.failing_songs)

    def test_bad_chord_quality(self):
        bad_chord_quality = "am"
        res = whsongbook.parse.parse_chord("BadChordQuality", bad_chord_quality)
        self.assertTrue("BadChordQuality" in whsongbook.failing_songs)

    def test_good_chord_quality(self):
        good_chord_quality = "a:sus2"
        res = whsongbook.parse.parse_chord("GoodChordQuality", good_chord_quality)
        self.assertFalse("GoodChordQuality" in whsongbook.failing_songs)

    def test_bad_chord_inverstion(self):
        bad_chord_inverstion = "c/g:m"
        res = whsongbook.parse.parse_chord("BadChordInverstion", bad_chord_inverstion)
        self.assertTrue("BadChordInverstion" in whsongbook.failing_songs)

    def test_good_chord_inverstion(self):
        good_chord_inverstion = "c/g"
        res = whsongbook.parse.parse_chord("GoodChordInverstion", good_chord_inverstion)
        self.assertFalse("GoodChordInverstion" in whsongbook.failing_songs)

    def test_bad_chord(self):
        # TODO: Revisit after incorporating the new function "parse_chord"
        whsongbook.parse.parse_text("BadChord", """verse:
    [h]Early in the evenin' [A#5]just about supper [c]time """)
        self.assertEqual(whsongbook.failing_songs[-1], "BadChord")

if __name__ == "__main__":
    unittest.main()
