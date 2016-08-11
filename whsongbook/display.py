import logging
import re
from . import failing_songs

# Initialize global display variables
ACCIDENTALS = {"f": "b", "s": "#"}


def display_lyrics(lyrics):
    lyrics = lyrics or "\xA0"
    if lyrics.endswith(" "):
        lyrics = lyrics[:-1] + "\xA0"
    return lyrics


def display_lyrics(lyrics):
    return lyrics.replace(" ", "\xA0") or "\xA0\xA0"


def display_chord(filename, chord):
    ret = ""

    # Do not alter false chords
    if type(chord) != dict:
        ret = chord

    # Format chord dictionaries
    else:
        # Throw error if no root
        if not chord["root"]:
            logging.error("Undisplayable chord (%s) in file (%s). No root." %
                          (chord, filename))
            failing_songs.append(filename)

        else:
            ret += chord["root"].upper()
            if chord.get("accidental"):
                for k, v in ACCIDENTALS.items():
                    if chord["accidental"] == k:
                        ret += v
            if chord.get("quality"):
                ret += chord["quality"]
            if chord.get("interval"):
                ret += chord["interval"]
            if chord.get("add"):
                if "-" in chord["add"]:
                    ret += "(b%s)" % chord["add"][:-1]
                elif "+" in chord["add"]:
                    ret += "(#%s)" % chord["add"][:-1]
                else:
                    ret += "add" + chord["add"]
            if chord.get("inversion"):
                ret += "/" + chord["inversion"].upper()
            if chord.get("inversion_accidental"):
                for k, v in ACCIDENTALS.items():
                    if chord["inversion_accidental"] == k:
                        ret += v

    return ret


def display_section_name(name):
    ret = "(%s)" % (name.title())
    return ret
