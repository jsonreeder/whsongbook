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
    if chord[:1] == "(":
        ret = chord
    else:
        note = chord[:1]
        accidental = ""
        extension = ""
        slash = ""
        if ":" in chord:
            pre, extension = chord.split(":")
        if len(chord) > 1:
            if chord[1] == "f":
                accidental = "b"
            elif chord[1] == "s":
                accidental = "#"
        if "/" in chord:
            slash_note = ""
            slash_accidental = ""
            pre, slash_chord = chord.split("/")
            slash_note = slash_chord[:1]
            if len(slash_chord) > 1:
                if slash_chord[1] == "f":
                    slash_accidental = "b"
                elif slash_chord[1] == "s":
                    slash_accidental = "#"
            slash = "/" + slash_note.upper() + slash_accidental

        ret = note.upper() + accidental + extension + slash
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
