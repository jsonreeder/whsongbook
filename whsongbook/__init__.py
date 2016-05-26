from logging import FileHandler, ERROR
import os
import re

from flask import Flask

app = Flask(__name__)
songs_data = []

from . import views

from .parse import *
from .display import *

# Configure logging
file_handler = FileHandler("app_errors.log")
file_handler.setLevel(ERROR)
app.logger.addHandler(file_handler)

def check_type(data):
    return isinstance(data, list)

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

