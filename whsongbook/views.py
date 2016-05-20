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
    songs_dir = "songs/production/"
    songs = listdir(songs_dir)
    selection = choice(songs)
    return redirect("/songs/%s" % (selection[:-5]))

@app.route("/toc")
def songs():
    """
    List all songs in the production folder
    """

    songs_dir = "songs/production/"
    songs = []
    for song in listdir(songs_dir):
        no_extension = song[:-5]
        spaces = no_extension.replace("_", " ")
        caps = spaces.title()
        title, artist = caps.split("-")
        songs.append([no_extension, title, artist])

    # return render_template("song_fixed.html")
    return render_template("toc.html",
                           songs = songs
    )
    # songs_dir = "songs/production/"
    # return str(listdir(songs_dir))

@app.route("/songs/<title>")
def song(title):
    # Test with "http://0.0.0.0:8080/songs/i_will_follow_you_into_the_dark-death_cab_for_cutie"

    songs_dir = "songs/production/"
    full_title = songs_dir + title + ".song"
    sections = []
    metadata = {}
    cur = None

    with open(full_title, "r") as f:
        text = f.read()

    # Parse file
    for line in text.splitlines():
        # strip initial white space
        line = line.rstrip()
        # ignore blank lines
        if not line: continue

        # identify line type statements (ie "chorus:")
        if line == line.lstrip():
            cur = []
            sections.append((line.strip(":"), cur))

        # work with all remaining lines (content)
        else:
            line = line.strip()
            # separate chords from lyrics
            if "[" in line and "genres = " not in line:
                chord_sections = []
                for section in line.split("["):
                    if "]" in section:
                        chord, lyric = section.split("]", 1)
                        if " " in chord:
                            multi_chords = chord.split(" ")
                            for m in multi_chords:
                                chord_sections.append((m,""))
                        else:
                            chord_sections.append((chord, lyric))
                    elif section:
                        chord_sections.append(("", section))
                line = chord_sections
            cur.append(line)

    # convert header section to dictionary
    if sections[0][0] == "header":
        for line in sections.pop(0)[1]:
            key, value = line.split('=', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())

    # return str(sections)
    return render_template("song.html",
                           title=metadata['title'],
                           artist=metadata['artist'],
                           sections=sections
    )

@app.route("/songs_list")
def songs_list():
    ret = ""
    for song in songs_data:
        ret += str(song.metadata)
    return str(ret)
