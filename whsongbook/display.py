import logging
import re

logging.basicConfig(filename="song_errors.log", level=logging.ERROR)

def display_lyrics(lyrics):
    lyrics = lyrics or "\xA0"
    if lyrics.endswith(" "):
        lyrics = lyrics[:-1]+"\xA0"
    return lyrics

def display_lyrics(lyrics):
    return lyrics.replace(" ", "\xA0") or "\xA0\xA0"

def display_chords(chord):
    accidentals = {"f": "b", "s": "#"}

    # parse repeat signs as chords, eg (x3)
    if chord[:1] == "(":
        ret = chord

    # parse empty strings as chords
    elif len(chord) == 0:
        ret = chord

    # parse all other chords
    else:

        note = chord[:1]
        accidental = ""
        extension = ""
        slash = ""
        if ":" in chord:
            extension = re.split(":|/", chord)[1]
        if len(chord) > 1:
            for k,v in accidentals.items():
                if chord[1] == k:
                    accidental = v
        if "/" in chord:
            slash_note = ""
            slash_accidental = ""
            pre, slash_chord = chord.split("/")
            slash_note = slash_chord[:1]
            if len(slash_chord) > 1:
                for k,v in accidentals.items():
                    if slash_chord[1] == k:
                        slash_accidental = v
            slash = "/" + slash_note.upper() + slash_accidental

        ret = note.upper() + accidental + extension + slash

    return ret

def display_section_name(name):
    ret = "(%s)" % (name.title())
    return ret
