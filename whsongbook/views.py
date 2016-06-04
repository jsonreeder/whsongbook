import ast
from os import listdir
from random import choice
from flask import render_template, redirect
from . import app, songs_data, artists

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/random")
def random():
    # TODO: Refactor with new song urls
    selection = choice(songs_data).filename
    return redirect("/songs/%s" % (selection[:-5]))

@app.route("/browse")
def browse():
    songs = []
    for song in songs_data:
        title = song.metadata["title"]
        artist = song.metadata["artist"]
        link = "/browse/%s/%s" % (artist.replace(" ", "_"), title.replace(" ", "_"))
        songs.append([link, title, artist])

    return render_template("browse.html",
                           songs = sorted(songs, key=lambda song: song[1])
    )

@app.route("/browse/<artist_underscore>/<title_underscore>")
def song(artist_underscore, title_underscore):

    artist = artist_underscore.replace("_", " ")
    title = title_underscore.replace("_", " ")

    # test for urls to songs that do not exist
    try:
        selection = next(song for song in songs_data if song.metadata["title"]==title and song.metadata["artist"]==artist)
    except StopIteration:
        return redirect("/browse")

    return render_template("song.html",
                           filename=selection.filename,
                           title=title,
                           artist=artist,
                           sections=selection.content
    )


@app.route("/artists/<name>")
def artist(name):
    # TODO: Return to this, it is incomplete

    # Test for urls to artists that do not exist
    name = name.replace("_", " ")
    # lower_case_artists = [a.replace(" ", "_").lower() for a in artists]
    if name not in artists.keys():
        return redirect("/browse")
    else:
        songs = artists[name]
        return render_template("artist.html",
                                artist = name,
                                songs = songs
        )



@app.route("/songs_list")
def songs_list():
    ret = ""
    for song in songs_data:
        ret += str(song.metadata)
    return str(ret)
