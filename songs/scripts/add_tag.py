"""
Add Tag

Add a given tag to a given set of songs
"""

from os import listdir
import argparse

def validate_tag(tag):
    """
    Make sure that tag is among valid options
    """

    valid_tags = ["americana", "sing-along", "modern"]

    if tag not in valid_tags:
        print("ERROR: Invalid tag -- %s" % tag)
        return False

    return True


def validate_song(song):
    """
    Make sure that the song exists in the production directory
    """

    songs_directory_contents = listdir("../production")

    if song not in songs_directory_contents:
        print("ERROR: Song not found -- %s" % song)
        return False

    # Check for existing tags
    with open("../production/" + song, "r") as f:
        text = f.read()

        if "tags =" in text:
            print("ERROR: Song already has tags -- %s" % song)
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
        return False

    for song in songs:
        if not validate_song(song):
            return False

    for song in songs:
        with open("../production/" + song, "r") as f:
            old_text = f.read()

        new_text = add_tag(tag, old_text)

        with open("../production/" + song, "w") as f:
            f.write(new_text)
            # Add a blank line at the end
            f.write("\n")

    return True

if __name__ == "__main__":

    # Parse input
    parser = argparse.ArgumentParser(description='Add tags to songs')
    parser.add_argument('tag', metavar='T', type=str,
                    help='The tag to be added')
    args = parser.parse_args()

    # Get songs
    print("Enter/Paste songs. Ctrl-D to run (eshell: RET C-q C-d RET).\n")
    songs = []
    while True:
        try:
            line = input("")
        except EOFError:
            break
        songs.append(line)

    ## Allow for some poor formatting of songs
    better_songs = []
    for song in songs:
        song = song.strip()
        if song[-1] == ",":
            song = song[:-1]
        if song[-1] == "'":
            song = song[:-1]
        song = "%s" % song
        better_songs.append(song)

    # Add the tags
    main(args.tag, better_songs)
    print("Success")


def test_invalid_tag():
    assert validate_tag("Americana") == False

def test_valid_tag():
    assert validate_tag("americana") == True

def test_invalid_song():
    assert validate_song("Wildwood_Flower") == False

def test_valid_song():
    assert validate_song("Apeman_-_The_Kinks.song") == True

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
