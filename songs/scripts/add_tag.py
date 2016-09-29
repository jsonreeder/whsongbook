"""
Add Tag

Add a given tag to a given set of songs
"""

from os import listdir

def validate_tag(tag):
    """
    Make sure that tag is among valid options
    """

    valid_tags = ["americana"]

    if tag not in valid_tags:
        return False

    return True


def validate_song(song):
    """
    Make sure that the song exists in the production directory
    """

    songs_directory_contents = listdir("../production")

    if song not in songs_directory_contents:
        return False

    return True


def add_tag(tag, songs):
    """
    Add a given tag to a given set of songs
    """

    if not validate_tag(tag):
        print("ERROR: Invalid tag")
        return False

    for song in songs:
        if not validate_song(song):
            print("ERROR: Invalid song")
            return False

    return True

def test_invalid_tag():
    assert validate_tag("Americana") == False

def test_valid_tag():
    assert validate_tag("americana") == True

def test_invalid_song():
    assert validate_song("Wildwood_Flower") == False

def test_valid_song():
    assert validate_song("Wildwood_Flower_-_Maud_Irving.song") == True

def test_simple_tag_song():
    assert add_tag("americana", ["Wildwood_Flower_-_Maud_Irving.song"]) == True
