import os
import unittest

import whsongbook
from whsongbook.parse import *

class ParseTests(unittest.TestCase):

    def test_all_songs_good(self):
        """Parse all songs and make sure that none have failed."""

        songs_data = [whsongbook.parse.parse_file(file) for file in os.listdir("songs/production/")]
        self.assertFalse(whsongbook.failing_songs)

    def test_bad_section_name(self):
        bad_section_name = """
chors:
    [f]Down on the [c]corner, [g]out in the [c]street
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

    def test_bad_chord_add(self):
        bad_chord_add = "c:m7.5?"
        res = whsongbook.parse.parse_chord("BadChordAdd", bad_chord_add)
        self.assertTrue("BadChordAdd" in whsongbook.failing_songs)

    def test_good_chord_add(self):
        good_chord_add = "c:m.5-"
        res = whsongbook.parse.parse_chord("GoodChordAdd", good_chord_add)
        self.assertFalse("GoodChordAdd" in whsongbook.failing_songs)

    def test_bad_chord_interval(self):
        bad_chord_interval = "g:14"
        res = whsongbook.parse.parse_chord("BadChordInterval", bad_chord_interval)
        self.assertTrue("BadChordInterval" in whsongbook.failing_songs)

    def test_good_chord_interval(self):
        good_chord_interval = "g:7"
        res = whsongbook.parse.parse_chord("GoodChordInterval", good_chord_interval)
        self.assertFalse("GoodChordInterval" in whsongbook.failing_songs)

    def test_bad_chord_quality(self):
        bad_chord_quality = "a:min"
        res = whsongbook.parse.parse_chord("BadChordQuality", bad_chord_quality)
        self.assertTrue("BadChordQuality" in whsongbook.failing_songs)

    def test_good_chord_quality(self):
        good_chord_quality = "a:maj"
        res = whsongbook.parse.parse_chord("GoodChordQuality", good_chord_quality)
        self.assertFalse("GoodChordQuality" in whsongbook.failing_songs)

    def test_bad_chord_inversion(self):
        bad_chord_inversion = "c/g:m"
        res = whsongbook.parse.parse_chord("BadChordInversion", bad_chord_inversion)
        self.assertTrue("BadChordInversion" in whsongbook.failing_songs)

    def test_good_chord_inversion(self):
        good_chord_inversion = "c/g"
        res = whsongbook.parse.parse_chord("GoodChordInversion", good_chord_inversion)
        self.assertFalse("GoodChordInversion" in whsongbook.failing_songs)

    def test_bad_chord(self):
        whsongbook.parse.parse_text("BadChord", """verse:
    [h]Early in the evenin' [a:m]just about supper [c]time """)
        self.assertTrue("BadChord" in whsongbook.failing_songs)

if __name__ == "__main__":
    unittest.main()
