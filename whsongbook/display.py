"""
Display

This module formats the parsed data for proper display.
"""

import logging
from . import failing_songs

# Initialize global display variables
ACCIDENTALS = {"f": "b", "s": "#"}
LANGUAGE_INDICES = {"en": 0, "es": 1, "ar": 2}
LANGUAGE_NAMES = {"en": "English", "es": "Español", "ar": "عربي"}
SECTION_TRANSLATIONS = {"header": ("header", "header", "header"),
                        "verse": ("verse", "verso", "كوبليه"),
                        "pre-chorus":
                        ("pre-chorus", "pre-coro", "ما قبل اللازمة"),
                        "chorus": ("chorus", "coro", "اللازمة"),
                        "bridge": ("bridge", "puente", "bridge"),
                        "instrumental": ("instrumental", "instrumental",
                                         "instrumental"),
                        "notes": ("notes", "notes", "notes"),
                        "intro": ("intro", "intro", "intro"),
                        "interlude": ("interlude", "interludio", "interlude"),
                        "outro": ("outro", "outro", "outro")}


def display_lyrics(lyrics):
    """
    Format lyrics for display

    By replacing spaces with nonbreaking spaces, this method ensures that
    chords that have no associated lyrics are still displayed above the
    lyric line
    """

    ret = lyrics

    # Replace spaces with nonbreaking spaces
    ret = ret.replace(" ", "\xA0") or "\xA0\xA0"
    return ret


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


def connect_arabic(parsed_line):
    """
    For Arabic lyrics, add connecting character when connections are
    otherwise broken by HTML sections
    """
    ret = parsed_line

    # Ignore lines with no chords
    if isinstance(parsed_line, list):
        line_length = len(parsed_line)
        add_lam = False

        for chunk_num, chunk in enumerate(parsed_line):
            # Ignore chunks at the end of lines
            if chunk_num + 1 < line_length:

                # Ignore chunks followed only by a chord
                next_lyric = parsed_line[chunk_num + 1][1]
                if next_lyric:

                    chord, lyric = chunk
                    new_lyric = lyric

                    # Check for lam + alif (these cannot be joined simply by JOINER)
                    if add_lam:
                        new_lyric = "ل" + new_lyric
                        add_lam = False

                    if new_lyric[-1] == "ل" and next_lyric[0] in "اآأإ":
                        new_lyric = new_lyric[:-1]
                        add_lam = True

                    # Add ZERO WIDTH JOINER
                    new_lyric += "‍"

                    ret[chunk_num] = (chord, new_lyric)

    return ret


def display_language_name(lang_abbreviation):
    """
    Return the correct display name for a given language
    """

    return LANGUAGE_NAMES[lang_abbreviation]
