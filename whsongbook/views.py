from . import app, songs_data
from flask import render_template, redirect
from os import listdir
from random import choice
import ast

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/random")
def random():
    selection = choice(songs_data).filename
    return redirect("/songs/%s" % (selection[:-5]))

@app.route("/browse")
def browse():
    songs = []
    for song in songs_data:
        no_extension = song.filename[:-5]
        title = song.metadata["title"]
        artist = song.metadata["artist"]
        songs.append([no_extension, title, artist])

    return render_template("browse.html",
                           songs = songs
    )

@app.route("/songs/<title>")
def song(title):
    try:
        selection = next(song for song in songs_data if song.filename[:-5]==title)
    except StopIteration:
        return redirect({{ url_for(browse) }})

    return render_template("song.html",
                           title=selection.metadata['title'],
                           artist=selection.metadata['artist'],
                           sections=selection.content
    )

@app.route("/songs_list")
def songs_list():
    ret = ""
    for song in songs_data:
        ret += str(song.metadata)
    return str(ret)
