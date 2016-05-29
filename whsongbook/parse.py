import logging
import ast
import re
from . import failing_songs

logging.basicConfig(filename="song_errors.log", level=logging.ERROR)

# Acceptable syntax

## Sections
SECTION_NAMES = ["header", "verse", "chorus", "bridge", "instrumental", "notes"]

## Chords

class Song:

    def __init__(self, filename, metadata, content):
        self.filename = filename
        self.metadata = metadata
        self.content = content

def check_chord(chord):
    """
    Check that chords are in the right format.
    """

    # allow anything in parentheses (eg "(x3)")
    if chord[:1] == "(":
        pass

    # allow empty strings (for lyrics with no chords)
    elif len(chord) == 0:
        pass

    # reject unparsable characters
    else:
        try:
            parsable = "[a-gsuim1-9:/\|]+"
            assert(re.fullmatch(parsable, chord) != None)
        except AssertionError:
            return False

    return True

def parse_header(header):
    """
    TODO: This function is unused and incomplete
    Parse header and check that metadata is in the right format
    """

    parsable = ["title", "artist", "genres", "year", "capo"]

    metadata = []
    for line in header:
        try:
            key, value = line.split('=', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())
        except ValueError:
            return (False, False)

    return metadata

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

        # strip initial white space
        line = line.rstrip()

        # ignore blank lines
        if not line: continue

        # identify section definitions (ie "chorus:")
        if line == line.lstrip():
            section_name = line.strip(":")

            # log error if section is not recognized
            if section_name not in SECTION_NAMES:
                logging.error("Unrecognized section name (%s) in file (%s). Recognized sections are: %s." % (section_name, filename, ", ".join(sorted(SECTION_NAMES))))
                failing_songs.append(filename)

            cur = []
            sections.append((line.strip(":"), cur))

        # work with all remaining lines (content)
        else:
            line = line.strip()

            # separate chords from lyrics
            if "[" in line and "=" not in line:
                chord_sections = []

                # log error if unmatched bracket
                if line.count("[") != line.count("]"):
                    logging.error("Unmatched bracket in line (%s) in file (%s)" % (line, filename))
                    failing_songs.append(filename)

                for section in line.split("["):

                    if "]" in section:
                        chord, lyric = section.split("]", 1)

                        # parse multi chords (chords with spaces)
                        if " " in chord:
                            multi_chords = chord.split(" ")
                            for m in multi_chords:
                                chord_sections.append((m,""))
                        else:
                            chord_sections.append((chord, lyric))
                    elif section:
                        chord_sections.append(("", section))

                # throw error if chord not recognized
                for chord, lyric in chord_sections:
                    if not check_chord(chord):
                        logging.error("Unparsable chord (%s) in file (%s)" % (chord, filename))
                        failing_songs.append(filename)
                line = chord_sections

            cur.append(line)

    # convert header section to dictionary
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

    # return str(sections)
    return Song(filename, metadata, sections)
