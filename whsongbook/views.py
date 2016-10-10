"""
Views

This module defines the endpoints of the Flask app.
"""

from random import choice
from collections import defaultdict
from flask import render_template, redirect
from whoosh.fields import *
from . import app, songs_data, artists_data, tags_data, ix


@app.route("/")
def home():
    """
    Display the home page.
    """

    return render_template("index.html")


@app.route("/about")
def about():
    """
    Display the about page.
    """

    return render_template("about.html")


@app.route("/random")
def random():
    """
    Redirect to a randomly selected song page.
    """

    selection = choice(songs_data)
    return redirect(selection.get_song_link())


@app.route("/browse")
def browse():
    """
    Display a list of links to all songs.
    """

    return render_template(
        "browse.html",
        songs=sorted(
            songs_data, key=lambda song: song.get_title()),
        header="All Songs")


@app.route("/browse/<artist_underscore>/<title_underscore>")
def song(artist_underscore, title_underscore):
    """
    Display a specific song transcription.
    """

    artist = artist_underscore.replace("_", " ")
    title = title_underscore.replace("_", " ")

    # test for urls to songs that do not exist
    try:
        selection = next(
            song for song in songs_data
            if song.get_title() == title and song.get_artist() == artist)
    except StopIteration:
        return redirect("/browse")

    return render_template("song.html", song=selection)


@app.route("/browse/<artist_underscore>")
def artist(artist_underscore):
    """
    Display a page for each artist, with a list of links to their songs.
    """

    artist = artist_underscore.replace("_", " ")

    # test for urls to artists that do not exist
    if artist not in artists_data.keys():
        return redirect("/browse")
    else:
        songs = [song for song in artists_data[artist]]
        header = artist.title()
        return render_template("browse.html", songs=songs, header=header)


@app.route("/tags")
def tags_page():
    """
    Display a single page containing all tags with links to their individual
    tag pages
    """

    tags = []
    for tag in sorted(tags_data.keys()):
        cur = defaultdict(list)
        cur["display"] = tag.title()
        cur["link"] = "/tags/%s" % tag
        tags.append(cur)

    return render_template("tags.html", tags=tags)


@app.route("/tags/<tag>")
def tag_page(tag):
    """
    Display a page for each tag, with a list of all songs in that tag.
    """

    if tag not in tags_data.keys():
        return redirect("/browse")
    else:
        songs = [song for song in tags_data[tag]]
        header = tag.title()
        return render_template("browse.html", songs=songs, header=header)


@app.route("/songs_list")
def songs_list():
    """
    Display the list of songs and metadata.
    """

    return str([song.get_metadata() for song in songs_data])


@app.route("/songs_data")
def display_songs_data():
    """
    Display a list of all song content and metadata.
    """

    return str([song.get_json() for song in songs_data])


@app.route("/search")
def search():
    """
    Search for songs.
    """

    from whoosh.qparser import QueryParser
    with ix.searcher() as searcher:
        query = QueryParser("artist", ix.schema).parse("Bob")
        results = searcher.search(query)
        titles = [result["title"] for result in results]

    return render_template("search.html", results=titles)
