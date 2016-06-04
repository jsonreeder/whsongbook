from . import app, songs_data, artists
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

@app.route("/browse_old")
def browse_old():
    songs = []
    for song in songs_data:
        no_extension = song.filename[:-5]
        title = song.metadata["title"]
        artist = song.metadata["artist"]
        songs.append([no_extension, title, artist])

    return render_template("browse.html",
                           songs = sorted(songs, key=lambda song: song[1])
    )

@app.route("/browse")
def browse():
    songs = []
    for song in songs_data:
        title = song.metadata["title"]
        artist = song.metadata["artist"]
        link = "%s__-__%s" % (title.replace(" ", "_"), artist.replace(" ", "_"))
        songs.append([link, title, artist])

    return render_template("browse.html",
                           songs = sorted(songs, key=lambda song: song[1])
    )
@app.route("/songs_old/<title>")
def song_old(title):

    # test for urls to songs that do not exist
    try:
        selection = next(song for song in songs_data if song.filename[:-5]==title)
    except StopIteration:
        # return redirect({{ url_for(browse) }})
        return redirect("/browse")

    return render_template("song.html",
                           filename=selection.filename,
                           title=selection.metadata['title'],
                           artist=selection.metadata['artist'],
                           sections=selection.content
    )

@app.route("/songs/<title_artist>")
def song(title_artist):

    title_nospace, artist_nospace = title_artist.split("__-__")
    title = title_nospace.replace("_", " ")
    artist = artist_nospace.replace("_", " ")

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
