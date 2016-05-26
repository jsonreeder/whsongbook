from logging import FileHandler, ERROR
import logging
import os
import re
import ast

from flask import Flask

app = Flask(__name__)
songs_data = []

from . import views

# Configure logging
logging.basicConfig(filename="song_errors.log", level=logging.ERROR)
file_handler = FileHandler("app_errors.log")
file_handler.setLevel(ERROR)
app.logger.addHandler(file_handler)

def check_type(data):
    return isinstance(data, list)

def display_lyrics(lyrics):
    lyrics = lyrics or "\xA0"
    if lyrics.endswith(" "):
        lyrics = lyrics[:-1]+"\xA0"
    return lyrics

def display_lyrics(lyrics):
    return lyrics.replace(" ", "\xA0") or "\xA0\xA0"

def display_chords(chord):
    accidentals = {"f": "b", "s": "#"}

    # parse repeat signs as chords, eg (x3)
    if chord[:1] == "(":
        ret = chord

    # parse empty strings as chords
    elif len(chord) == 0:
        ret = chord

    # parse all other chords
    else:
        # check for unparsable characters
        try:
            parsable = "[a-gsuim1-9:/\|]+"
            assert(re.fullmatch(parsable, chord) != None)
        except AssertionError:
            logging.error("Unparsable chord: %s" % (chord))
            return False

        note = chord[:1]
        accidental = ""
        extension = ""
        slash = ""
        if ":" in chord:
            extension = re.split(":|/", chord)[1]
        if len(chord) > 1:
            for k,v in accidentals.items():
                if chord[1] == k:
                    accidental = v
        if "/" in chord:
            slash_note = ""
            slash_accidental = ""
            pre, slash_chord = chord.split("/")
            slash_note = slash_chord[:1]
            if len(slash_chord) > 1:
                for k,v in accidentals.items():
                    if slash_chord[1] == k:
                        slash_accidental = v
            slash = "/" + slash_note.upper() + slash_accidental

        ret = note.upper() + accidental + extension + slash

    return ret

def display_section_name(name):
    ret = "(%s)" % (name.title())
    return ret

class Song:

    def __init__(self, filename, metadata, content):
        self.filename = filename
        self.metadata = metadata
        self.content = content

def parse_file(filename):
    songs_dir = "songs/production/"
    full_title = songs_dir + filename
    sections = []
    metadata = {}
    cur = None

    with open(full_title, "r") as f:
        text = f.read()

    for line in text.splitlines():
        # strip initial white space
        line = line.rstrip()
        # ignore blank lines
        if not line: continue

        # identify line type statements (ie "chorus:")
        if line == line.lstrip():
            cur = []
            sections.append((line.strip(":"), cur))

        # work with all remaining lines (content)
        else:
            line = line.strip()
            # separate chords from lyrics
            if "[" in line and "genres = " not in line:
                chord_sections = []
                for section in line.split("["):
                    if "]" in section:
                        chord, lyric = section.split("]", 1)
                        if " " in chord:
                            multi_chords = chord.split(" ")
                            for m in multi_chords:
                                chord_sections.append((m,""))
                        else:
                            chord_sections.append((chord, lyric))
                    elif section:
                        chord_sections.append(("", section))
                line = chord_sections
            cur.append(line)

    # convert header section to dictionary
    if sections[0][0] == "header":
        for line in sections.pop(0)[1]:
            key, value = line.split('=', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())

    # return str(sections)
    return Song(filename, metadata, sections)

def load_songs():
    global songs_data
    songs_dir = "songs/production/"
    for file in os.listdir(songs_dir):
        songs_data.append(parse_file(file))
    return songs_data

load_songs()

app.jinja_env.globals.update(
    check_type = check_type,
    display_lyrics = display_lyrics,
    display_chords = display_chords,
    display_section_name = display_section_name
)

