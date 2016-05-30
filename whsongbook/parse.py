import logging
import ast
import re
from . import failing_songs

logging.basicConfig(filename="song_errors.log", level=logging.ERROR)

# Initialize variables for acceptable song syntax

SECTION_NAMES = ["header", "verse", "chorus", "bridge", "instrumental", "notes"]
PITCHES = "[a-g]"
ACCIDENTALS = ["f", "s"]
DURATIONS = "^[0-9]+$"
QUALITIES = ["maj", "m", "dim", "aug", "sus"]
INTERVALS = "[1-9][0-3]"
ADDS = "[0-9-]+"

class Song:

    def __init__(self, filename, metadata, content):
        self.filename = filename
        self.metadata = metadata
        self.content = content

def check_chord(chord):
    """Check that chords are in the right format."""

    # Allow anything in parentheses (eg "(x3)")
    if chord[:1] == "(":
        pass

    # Allow empty strings (for lyrics with no chords)
    elif len(chord) == 0:
        pass

    # Reject unparsable characters
    else:
        try:
            parsable = "[a-gsuim1-9:/\|]+"
            assert(re.fullmatch(parsable, chord) != None)
        except AssertionError:
            return False

    return True

def parse_pitch(filename, pitch):
    """Parse pitches in LilyPond syntax."""

    pitch_temp = pitch
    pitch_dict = {"note": "",
                  "accidental": "",
                  "duration": ""
    }

    # Parse note
    if re.match(PITCHES, pitch_temp[0]):
        pitch_dict["note"] = pitch_temp[0]
        pitch_temp = pitch_temp[1:]
    else:
        logging.error("Unrecognized pitch (%s) in file (%s)." % (pitch, filename))
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
                logging.error("Unrecognized pitch duration (%s) in pitch (%s) in file (%s)." % (pitch_temp, pitch, filename))
                failing_songs.append(filename)

    return pitch_dict

def parse_chord(filename, chord):
    """Parse chords in LilyPond syntax."""

    chord_list = re.split("[:/]", chord)
    chord_dict = {"root": "",
                  "accidental": "",
                  "duration": "",
                  "quality": "",
                  "inversion": "",
                  "inversion_accidental": ""
    }


    # Parse root
    root_dict = parse_pitch(filename, chord_list.pop(0))
    chord_dict["root"] = root_dict["note"]
    chord_dict["accidental"] = root_dict["accidental"]
    chord_dict["duration"] = root_dict["duration"]

    # Parse quality
    if ":" in chord:
        chord_dict["quality"] = chord_list.pop(0)

    # Parse inverstion
    if "/" in chord:
        inverstion_dict = parse_pitch(filename, chord_list.pop(0))
        chord_dict["inversion"] = inverstion_dict["note"]

    return chord_dict

def parse_file(filename):
    songs_dir = "songs/production/"
    full_title = songs_dir + filename

    with open(full_title, "r") as f:
        text = f.read()

    return parse_text(filename, text)

def parse_text(filename, text):
    sections = []
    metadata = {}
    cur = None

    for line in text.splitlines():

        # Strip initial white space
        line = line.rstrip()

        # Ignore blank lines
        if not line: continue

        # Identify section definitions (ie "chorus:")
        if line == line.lstrip():
            section_name = line.strip(":")

            # Log error if section is not recognized
            if section_name not in SECTION_NAMES:
                logging.error("Unrecognized section name (%s) in file (%s). Recognized sections are: %s." % (section_name, filename, ", ".join(sorted(SECTION_NAMES))))
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
                    logging.error("Unmatched bracket in line (%s) in file (%s)" % (line, filename))
                    failing_songs.append(filename)

                for section in line.split("["):

                    # Parse lines with both lyrics and chords
                    if "]" in section:
                        chord, lyric = section.split("]", 1)

                        # Parse multi chords (chords separated by spaces)
                        if " " in chord:
                            multi_chords = chord.split(" ")
                            for m in multi_chords:
                                chord_sections.append((m,""))
                        else:
                            chord_sections.append((chord, lyric))

                    # Parse lines with only lyrics
                    elif section:
                        chord_sections.append(("", section))

                # Throw error if chord not recognized
                # TODO: Add more robust chord parsing here
                for chord, lyric in chord_sections:
                    if not check_chord(chord):
                        logging.error("Unparsable chord (%s) in file (%s)" % (chord, filename))
                        failing_songs.append(filename)
                line = chord_sections

            cur.append(line)

    # Convert header section to dictionary
    if sections[0][0] == "header":
        for line in sections.pop(0)[1]:

            # Check for lines without equals
            try:
                key, value = line.split('=', 1)
            except ValueError:
                logging.error("Unparsable header line (%s) in file (%s). Missing an equals sign." % (line, filename))
                failing_songs.append(filename)
            try:
                metadata[key.strip()] = ast.literal_eval(value.strip())

            # Catch errors in variable definition
            except SyntaxError:
                logging.error("Unparsable header line (%s) in file (%s). Make sure that types are defined correctly (i.e. that strings are in quotes, lists are in brackets, etc.)" % (line, filename))
                failing_songs.append(filename)
                metadata[key.strip()] = ""

    return Song(filename, metadata, sections)
