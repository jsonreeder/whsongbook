from . import app
from flask import render_template
from os import listdir
import re

@app.route("/")
def home():
    return render_template("song_fixed.html")

@app.route("/songs")
def songs():
    """
    List all songs in the production folder
    """

    songs_dir = "songs/production/"
    return str(listdir(songs_dir))

@app.route("/songs/<title>")
def song(title):
    # Test with "http://0.0.0.0:8080/songs/i_will_follow_you_into_the_dark-death_cab_for_cutie"

    songs_dir = "songs/production/"
    full_title = songs_dir + title + ".song"
    with open(full_title, "r") as f:
        # parse header
        
        return f.read()
