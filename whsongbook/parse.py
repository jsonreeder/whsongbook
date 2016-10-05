"""
Parse

This module defines the functions to parse the .song files.
"""

import logging
import ast
import re
import pprint
from . import failing_songs

# Initialize variables for acceptable song syntax
SECTION_NAMES = ["header", "verse", "pre-chorus", "chorus", "bridge",
                 "instrumental", "notes", "intro", "interlude", "outro"]
PITCHES = "[a-g]"
ACCIDENTALS = ["f", "s"]
DURATIONS = "^[0-9]+$"
QUALITIES = "^(maj|m|dim|aug|sus)$"
INTERVALS = "^[1-9][0-3]?$"
ADDS = "^\d+[+-]?$"
FALSE_CHORDS = "\(.+\)|\s|\|"


class Song:
    """
    Objects for parsed song trascriptions
    """

    def __init__(self, filename, metadata, content):
        self.filename = filename
        self.metadata = metadata
        self.content = content

    def __str__(self):
        ret = "Song Object:\n"
        ret += "Filename =  %s\n" % self.filename
        ret += "Metadata = %s\n" % self.metadata
        ret += "Content = %s\n" % pprint.pformat(self.content)
        return ret

    def get_json(self):
        """
        Return the content of the song object formatted for JSON
        """

        return {self.filename: {"metadata": self.metadata,
                                "content": self.content}}

    def get_lyrics(self):
        """
        Return the title, metadata, and lyrics of the song object formatted for JSON
        TODO: Implement
        """


def parse_pitch(filename, pitch):
    """
    Parse pitches notated in LilyPond syntax.
    Pitches are the notes a:g including sharps and flats.
    Pitches are distinct from chords, which are extensions on the above notes.
    """

    pitch_temp = pitch
    pitch_dict = {"note": "", "accidental": "", "duration": ""}

    # Parse note
    if re.match(PITCHES, pitch_temp):
        pitch_dict["note"] = pitch_temp[0]
        pitch_temp = pitch_temp[1:]
    else:
        logging.error("Unrecognized pitch (%s) in file (%s)." %
                      (pitch, filename))
        failing_songs.append(filename)
        return pitch_dict

    # Parse accidental and duration
    if pitch_temp:
        # Parse accidental
        if pitch_temp[0] in ACCIDENTALS:
            pitch_dict["accidental"] = pitch_temp[0]
            pitch_temp = pitch_temp[1:]

        # Parse duration
        if pitch_temp:
            if re.match(DURATIONS, pitch_temp):
                pitch_dict["duration"] = pitch_temp
            else:
                logging.error(
                    "Unrecognized pitch duration (%s) in pitch (%s) in file (%s)."
                    % (pitch_temp, pitch, filename))
                failing_songs.append(filename)

    return pitch_dict


def parse_chord(filename, chord):
    """
    Parse chords in LilyPond syntax.
    Chords consist of notes (a:g) and optional extensions (:m, :dim, etc.).
    """

    # Ignore empty and "false chords" eg (x2)
    if not chord:
        return

    elif re.match(FALSE_CHORDS, chord):
        return chord

    # Parse normal chords
    else:
        chord_list = re.split("[:/]", chord)
        chord_dict = {"root": "",
                      "accidental": "",
                      "duration": "",
                      "quality": "",
                      "interval": "",
                      "add": "",
                      "inversion": "",
                      "inversion_accidental": ""}

        # Parse root
        root_dict = parse_pitch(filename, chord_list.pop(0))
        chord_dict["root"] = root_dict["note"]
        chord_dict["accidental"] = root_dict["accidental"]
        chord_dict["duration"] = root_dict["duration"]

        # Parse quality
        if ":" in chord:
            temp_quality = chord_list.pop(0)

            # split off add
            if "." in temp_quality:
                temp_add_list = temp_quality.split(".")
                temp_quality = temp_add_list[0]
                temp_add = temp_add_list[1]
                if re.match(ADDS, temp_add):
                    chord_dict["add"] = temp_add
                else:
                    logging.error(
                        "Unparsable add (%s) in chord (%s) in file (%s)." %
                        (temp_add, chord, filename))
                    failing_songs.append(filename)

            # split off interval
            if re.search("\d+", temp_quality):
                temp_interval_list = re.split("(\d+)", temp_quality)
                temp_quality = temp_interval_list[0]
                temp_interval = temp_interval_list[1]
                if re.match(INTERVALS, temp_interval):
                    chord_dict["interval"] = temp_interval
                else:
                    logging.error(
                        "Unparsable interval (%s) in chord (%s) in file (%s)."
                        % (temp_interval, chord, filename))
                    failing_songs.append(filename)

            # remaining text should be the quality
            if temp_quality:
                if re.search(QUALITIES, temp_quality):
                    chord_dict["quality"] = temp_quality
                else:
                    logging.error(
                        "Unparsable quality (%s) in chord (%s) in file (%s)." %
                        (temp_quality, chord, filename))
                    failing_songs.append(filename)

        # Parse inversion
        if "/" in chord:
            inversion_dict = parse_pitch(filename, "".join(chord_list))
            chord_dict["inversion"] = inversion_dict["note"]
            chord_dict["inversion_accidental"] = inversion_dict["accidental"]

        return chord_dict


def parse_file(filename):
    """
    Parse .song files.
    """

    songs_dir = "songs/production/"
    full_title = songs_dir + filename

    with open(full_title, "r") as f:
        text = f.read()

    return parse_text(filename, text)


def parse_text(filename, text):
    """
    Parse the text in .song files.
    The text is distinct from the chords.
    """

    sections = []
    metadata = {}
    cur = None

    for line in text.splitlines():

        # Strip trailing white space
        line = line.rstrip()

        # Ignore blank lines
        if not line: continue

        # Identify section definitions (ie "chorus:")
        if line == line.lstrip():
            section_name = line.strip(":")

            # Log error if section is not recognized
            if section_name not in SECTION_NAMES:
                logging.error(
                    "Unrecognized section name (%s) in file (%s). Recognized sections are: %s."
                    %
                    (section_name, filename, ", ".join(sorted(SECTION_NAMES))))
                failing_songs.append(filename)

            cur = []
            sections.append((line.strip(":"), cur))

        # Work with all remaining lines (content)
        else:
            line = line.strip()

            # Separate chords from lyrics
            if "[" in line and "=" not in line:
                chord_sections = []

                # Log error if unmatched bracket
                if line.count("[") != line.count("]"):
                    logging.error("Unmatched bracket in line (%s) in file (%s)"
                                  % (line, filename))
                    failing_songs.append(filename)

                for section in line.split("["):

                    # Parse lines with both lyrics and chords
                    if "]" in section:
                        chord, lyric = section.split("]", 1)

                        # Parse multi chords (chords separated by spaces)
                        if " " in chord:
                            multi_chords = chord.split()
                            for m in multi_chords:
                                parsed_chord = parse_chord(filename, m)
                                chord_sections.append((parsed_chord, ""))

                        # Parse normal chords
                        else:
                            parsed_chord = parse_chord(filename, chord)
                            chord_sections.append((parsed_chord, lyric))

                    # Parse lines with only lyrics
                    elif section:
                        chord_sections.append(("", section))

                line = chord_sections

            cur.append(line)

    # Convert header section to dictionary

    # Assign "en" as default language
    metadata["language"] = "en"

    if sections[0][0] == "header":
        for line in sections.pop(0)[1]:

            # Check for lines without equals
            try:
                key, value = line.split('=', 1)
            except ValueError:
                logging.error(
                    "Unparsable header line (%s) in file (%s). Missing an equals sign."
                    % (line, filename))
                failing_songs.append(filename)
            try:
                metadata[key.strip()] = ast.literal_eval(value.strip())

            # Catch errors in variable definition
            except SyntaxError:
                logging.error(
                    "Unparsable header line (%s) in file (%s). Make sure that types are defined correctly (i.e. that strings are in quotes, lists are in brackets, etc.)"
                    % (line, filename))
                failing_songs.append(filename)
                metadata[key.strip()] = ""

    return Song(filename, metadata, sections)
