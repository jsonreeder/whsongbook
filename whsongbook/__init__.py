import os
import re

from flask import Flask

app = Flask(__name__)

from . import views

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
    note = re.sub("[0-9]|:.*", "", chord)
    extension = ""
    if ":" in chord:
        pre, extension = chord.split(":")
    ret = note.upper() + extension
    return ret

def display_section_name(name):
    ret = "(%s)" % (name.title())
    return ret

app.jinja_env.globals.update(
    check_type = check_type,
    display_lyrics = display_lyrics,
    display_chords = display_chords,
    display_section_name = display_section_name
)
