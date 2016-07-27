import re

# Initialize gloabls
infile = "junk_in.txt"
artist = ""
title = ""
out_text = ""
delimeter = "\\"
accidentals = {"#": "s", "b": "f"}

# Read file
with open(infile, "r") as f:
    text = f.read()

    # Strip whitespace
    text_stripped_list = [line.strip() for line in text.splitlines()]
    text_stripped = "\n".join(text_stripped_list)
    text = text_stripped

    # Split into parts
    sections = text.split("\n\n")
    parts = []
    c = 1
    for s in sections:
        name = "section_%s" % (c)
        lines = s.splitlines()
        parts.append({name: lines})
        c += 1

    # Parse parts
    parsed_parts = []
    for p in parts:
        for section_name, content in p.items():
            type = "verse"

            # Parse header
            if section_name == "section_1":
                type = "header"

            # Parse choruses
            if "(Chorus)" in content:
                type = "chorus"
                content = ""

            # Align chords with lyrics
            # Find sections with any chords
            if delimeter in str(content):
                if len(content) % 2 == 1:
                    print("WARNING: Uneven number of lines. Check chords here:")
                    [print("    " + line) for line in content]
                new_content = []
                i = 0
                while i < len(content) - 1:
                    chord_line = content[i]
                    lyric_line = content[i+1]

                    # For initial lines without delimeters, write straight away
                    if delimeter not in lyric_line:
                        new_content.append(chord_line)
                        new_content.append(lyric_line)

                    if delimeter in chord_line:
                        print("ERROR: This line was expected to be a lyric line:\n - %s" % (lyric_line))

                    # For the lines with delimeters, align
                    else:
                        chords = chord_line.split()
                        # Check to see that all chords have a place to go
                        if lyric_line.count(delimeter) != len(chords):
                            print("ERROR: Unparsable line. No. of chords (%d) != no. of delimeters (%d).\n - Chords: %s\n - Line: %s" % (len(chords), lyric_line.count(delimeter), chords, lyric_line))


                        # Parse chords
                        new_chords = []
                        for c in chords:
                            new_chord = ''
                            c = re.sub("[()]", "", c)
                            for q, c in enumerate(list(c)):
                                if q == 0:
                                    new_chord += c
                                elif c in accidentals.keys():
                                    new_chord += accidentals[c]
                                elif c:
                                    if ":" not in new_chord:
                                        new_chord += ":"
                                    new_chord += "%s" % (c)
                                new_chord = new_chord.lower()
                            new_chords.append(new_chord)
                        chords = new_chords

                        lyrics = lyric_line
                        while len(chords) > 0:
                            chord = chords.pop(0)
                            lyrics = lyrics.replace(delimeter, "[%s]" % (chord), 1)

                    new_content.append(lyrics)
                    i += 2

                content = new_content

            parsed_parts.append((type, content))

    # Format
    for p in parsed_parts:
        type = p[0]
        content = p[1]

        if type == "header":
            out_text += "%s:\n" % (type)
            header_types = {0: "title", 1: "artist", 2: "capo"}
            for i, c in enumerate(content):
                if i == 0:
                    title = c
                    out_text += "    %s = \"%s\"\n" % ("title", title)
                elif i == 1:
                    artist = c
                    out_text += "    %s = \"%s\"\n" % ("artist", artist)
                elif "apo" in c:
                    digit = re.compile(r"[^\d]")
                    capo = int(digit.sub("", c))
                    out_text += "    %s = %d\n" % ("capo", capo)
                else:
                    out_text += "    %s = \"%s\"\n" % ("notes", c)

        # Chorus
        elif content == "":
            out_text += "%s\n" % type

        # Others
        else:
            out_text += "%s:\n" % type
            for line in content:
                out_text += "    %s\n" % line
        out_text += "\n"

# Remove trailing blank lines
out_text = out_text.strip()

# Remove line-final punctution
out_text_stripped = ""
for line in out_text.splitlines():
    if line.endswith(".") or line.endswith(","):
        out_text_stripped += line[:-1]
    else:
        out_text_stripped += line
    out_text_stripped += "\n"

# Write output
outfile = "%s - %s.song" % (title, artist)
outfile = outfile.replace(" ", "_")
with open(outfile, "w") as f:
    f.write(out_text_stripped)

# # Final check
if delimeter in out_text:
    print("ERROR: A delimeter was not parsed.")
else:
    print("SUCCESS: wrote %s" % (outfile))
