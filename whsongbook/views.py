"""
Views

This module defines the endpoints of the Flask app.
"""

from random import choice
from collections import defaultdict
from flask import render_template, redirect
from . import app, songs_data, artists_data, tags_data, languages_data, display, ix


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
    Display a list of paths to groups of songs.
    """

    return render_template("browse.html")


@app.route("/songs")
def songs():
    """
    Display a list of links to all songs.
    """

    return render_template(
        "buttons.html",
        songs=sorted(
            songs_data, key=lambda song: song.get_title()),
        header="Songs",
        parent="Browse",
        show_artist=True,
        contains_song_objects=True)


@app.route("/songs/<artist_underscore>/<title_underscore>")
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
        return redirect("/songs")

    return render_template("song.html", song=selection)


@app.route("/artists")
def artists():
    """
    Display a list of links to all artists.
    """

    artists = []
    for artist in sorted(artists_data.keys()):
        cur = defaultdict(list)
        cur["display"] = artist.title()
        cur["link"] = "/artists/%s" % artist.replace(" ", "_")
        artists.append(cur)

    return render_template(
        "buttons.html",
        items=artists,
        header="Artists",
        parent="Browse",
        contains_song_objects=False)


@app.route("/artists/<artist_underscore>")
def artist(artist_underscore):
    """
    Display a page for each artist, with a list of links to their songs.
    """

    artist = artist_underscore.replace("_", " ")
    path = "/artists"
    parent = "Artists"

    # test for urls to artists that do not exist
    if artist not in artists_data.keys():
        return redirect("/artists")
    else:
        songs = [song for song in artists_data[artist]]
        header = artist.title()
        return render_template(
            "buttons.html",
            songs=songs,
            header=header,
            path=path,
            parent=parent,
            show_artist=False,
            contains_song_objects=True)


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

    return render_template(
        "buttons.html",
        items=tags,
        header="Tags",
        parent="Browse",
        contains_song_objects=False)


@app.route("/tags/<tag>")
def tag_page(tag):
    """
    Display a page for each tag, with a list of all songs in that tag.
    """

    path = "/tags"
    parent = "Tags"
    if tag not in tags_data.keys():
        return redirect("/tags")
    else:
        songs = [song for song in tags_data[tag]]
        header = tag.title()
        return render_template(
            "buttons.html",
            songs=songs,
            header=header,
            path=path,
            parent=parent,
            show_artist=True,
            contains_song_objects=True)


@app.route("/languages")
def languages_page():
    """
    Display a single page containing all languages with links to their individual
    language pages
    """

    languages = []
    for language in sorted(languages_data.keys()):
        cur = defaultdict(list)
        cur["display"] = display.display_language_name(language)
        cur["link"] = "/languages/%s" % language
        languages.append(cur)

    return render_template(
        "buttons.html",
        items=sorted(
            languages, key=lambda language: language["display"]),
        header="Languages",
        parent="Browse",
        contains_song_objects=False)


@app.route("/languages/<language>")
def language_page(language):
    """
    Display a page for each language, with a list of all songs in that language.
    """

    path = "/languages"
    parent = "Languages"
    if language not in languages_data.keys():
        return redirect(parent)
    else:
        songs = [song for song in languages_data[language]]
        header = display.display_language_name(language)
        return render_template(
            "buttons.html",
            songs=songs,
            header=header,
            path=path,
            parent=parent,
            show_artist=True,
            contains_song_objects=True)


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
        query = QueryParser("title", ix.schema).parse("document")
        results = searcher.search(query)

    return render_template("search.html", results=results)
