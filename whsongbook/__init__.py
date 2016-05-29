from logging import FileHandler, ERROR
from flask import Flask
import os
import re

app = Flask(__name__)
failing_songs = []

from . import parse, display

songs_data = [parse.parse_file(file) for file in os.listdir("songs/production/")]

from . import views

# Configure logging
file_handler = FileHandler("app_errors.log")
file_handler.setLevel(ERROR)
app.logger.addHandler(file_handler)

def check_type(data):
    return isinstance(data, list)

app.jinja_env.globals.update(
    check_type = check_type,
    display_lyrics = display.display_lyrics,
    display_chords = display.display_chords,
    display_section_name = display.display_section_name
)

