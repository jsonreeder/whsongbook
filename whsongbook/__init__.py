import os
import re
import logging
from collections import defaultdict
from flask import Flask

# logging.basicConfig(filename="errors.log", level=logging.ERROR)
logging.basicConfig(filename="errors.log", level=logging.DEBUG)
app = Flask(__name__)
failing_songs = []

from . import parse, display

# Load songs
songs_data = [parse.parse_file(file) for file in os.listdir("songs/production/")]
logging.debug("Songs Data:\n")
for i in songs_data:
    logging.debug(i)


# Die if any songs fail to parse
if failing_songs:
    import sys
    sys.exit(1)

# Build list of artists and their songs
artists = defaultdict(list)
for s in songs_data:
    artists[s.metadata["artist"]].append(s.metadata["title"])

from . import views

def check_type(data):
    return isinstance(data, list)

app.jinja_env.globals.update(
    check_type = check_type,
    display_lyrics = display.display_lyrics,
    display_chord = display.display_chord,
    display_section_name = display.display_section_name
)

