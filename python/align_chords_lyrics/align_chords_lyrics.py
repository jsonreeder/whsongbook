import re

# sample input
string_sample_chords = """
c1 a:m f c2 g
c1 a:m f c2 g \break
"""

list_sample_chords = ["c1", "a:m", "f", "c2", "g", "c1", "a:m", "f", "c2", "g"]

sample_lyrics = """
[]Love of mine some day []you will die
But I'll be []close behind. I'll follow []you into the []dark,
No []blinding light or tunnels to []gates of white
Just our hands []clasped so tight, waiting []for the hint of a []spark.
"""

def match_chords_with_lyrics(chords, lyrics):
    """Match a set of chords with the text of lyrics"""

    output = ""

    for l in lyrics.splitlines():
        newline = ""
        for x in l.split("["):
            if "]" in x:
                newsection = "[%s%s" % (chords.pop(0), x)
            else:
                newsection = x
            newline += newsection
        output += newline + "\n"

    return output

def chords_to_list(chords):
    "Convert a string of chords to a list"

    words_to_remove = "\break|\d|:"

    string_without = re.sub(words_to_remove, "", chords)

    list = string_without.split()

    cap_list = [x.title() for x in list]

    return cap_list

def chords_above(lyrics_with_chords):
    """Convert a string of lyrics with chords within brackets
    to a string of lyrics with chords above"""

    output = ""

    for l in lyrics_with_chords.splitlines():
        chord_line = ""
        lyric_line = ""

        for x in l.split("["):
            if "]" in x:
                chord, lyric = x.split("]")
                extra_space = " " * ( len(lyric) - len(chord) )
                chord_line += chord + extra_space
                lyric_line += lyric
            else:
                chord_line += " " * len(x)
                lyric_line += x

        output += chord_line + "\n"
        output += lyric_line + "\n"

    return output

chords = chords_to_list(string_sample_chords)
chords_with_lyrics = match_chords_with_lyrics(chords, sample_lyrics)

print(chords_above(chords_with_lyrics))
