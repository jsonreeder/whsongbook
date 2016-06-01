# from logging import FileHandler, ERROR
from flask import Flask
from collections import defaultdict
import os
import re
import logging

logging.basicConfig(filename="errors.log", level=logging.ERROR)
app = Flask(__name__)
failing_songs = []

from . import parse, display

# Load songs
songs_data = [parse.parse_file(file) for file in os.listdir("songs/production/")]

# Die if any songs fail to parse
if failing_songs:
    import sys
    sys.exit(1)

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

