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

def add_tag(tag, song):
    """
    Insert a tag into the header of a song
    """

    lines = song.splitlines()
    tag_to_insert = '    tags = ["%s"]' % tag
    insertion_location = 3
    lines.insert(insertion_location, tag_to_insert)

    return "\n".join(lines)

def main(tag, songs):
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

        else:
            with open("../production/" + song, "w") as f:
                file = f.read()

    return True

def test_invalid_tag():
    assert validate_tag("Americana") == False

def test_valid_tag():
    assert validate_tag("americana") == True

def test_invalid_song():
    assert validate_song("Wildwood_Flower") == False

def test_valid_song():
    assert validate_song("Wildwood_Flower_-_Maud_Irving.song") == True

def test_add_a_tag():
    sample_in = """header:
    title = "Wildwood Flower"
    artist = "Maud Irving"
    associated_artists = ["Joseph Philbrick Webster", "The Carter Family", "June Carter", "Johnny Cash"]
    genres = ["folk", "country", "bluegrass"]"""

    desired_out = """header:
    title = "Wildwood Flower"
    artist = "Maud Irving"
    tags = ["americana"]
    associated_artists = ["Joseph Philbrick Webster", "The Carter Family", "June Carter", "Johnny Cash"]
    genres = ["folk", "country", "bluegrass"]"""

    assert add_tag("americana", sample_in) == desired_out
