"""
Display

This module formats the parsed data for proper display.
"""

import logging
from . import failing_songs

# Initialize global display variables
ACCIDENTALS = {"f": "b", "s": "#"}
LANGUAGE_INDICES = {"en": 0, "es": 1, "ar": 2}
SECTION_TRANSLATIONS = {"header": ("header", "header", "header"),
                        "verse": ("verse", "verso", "كوبليه"),
                        "pre-chorus": ("pre-chorus", "pre-coro", "ما قبل اللازمة"),
                        "chorus": ("chorus", "coro", "اللازمة"),
                        "bridge": ("bridge", "puente", "bridge"),
                        "instrumental": ("instrumental", "instrumental", "instrumental"),
                        "notes": ("notes", "notes", "notes"),
                        "intro": ("intro", "intro", "intro"),
                        "interlude": ("interlude", "interludio", "interlude"),
                        "outro": ("outro", "outro", "outro")}


def display_lyrics(lyrics):
    lyrics = lyrics or "\xA0"
    if lyrics.endswith(" "):
        lyrics = lyrics[:-1] + "\xA0"
    return lyrics


def display_lyrics(lyrics):
    return lyrics.replace(" ", "\xA0") or "\xA0\xA0"


def display_chord(filename, chord):
    """
    Convert chords from LilyPond syntax (a:m) into display (Am)
    """

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


def display_section_name(name, language):
    """
    Find the proper display name for an abbreviated section
    given a song's language
    """

    language_index = LANGUAGE_INDICES[language]
    ret = SECTION_TRANSLATIONS[name][language_index]
    return "(%s)" % (ret.title())
