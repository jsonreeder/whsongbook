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
            if delimeter in str(content):
                new_content = []
                i = 0
                while i < len(content) - 1:
                    chord_line = content[i]
                    lyric_line = content[i+1]
                    if delimeter in lyric_line:

                        chords = chord_line.split()
                        # Check to see that all chords have a place to go
                        if lyric_line.count(delimeter) != len(chords):
                            print("ERROR: Unparsable line. No. of chords (%d) != no. of delimeters (%d).\n - Chords: %s\n - Line: %s" % (len(chords), lyric_line.count(delimeter), chords, lyric_line))


                        # Parse chords
                        new_chords = []
                        for c in chords:
                            new_chord = ''
                            for q, c in enumerate(list(c)):
                                if q == 0:
                                    new_chord += c.lower()
                                elif c in accidentals.keys():
                                    new_chord += accidentals[c]
                                elif c:
                                    if ":" not in new_chord:
                                        new_chord += ":"
                                    new_chord += "%s" % (c)
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
                elif i == 1:
                    artist = c
                out_text += "    %s = \"%s\"\n" % (header_types[i], c)

        # Chorus
        elif content == "":
            out_text += "%s\n" % type

        # Others
        else:
            out_text += "%s:\n" % type
            for line in content:
                out_text += "    %s\n" % line
        out_text += "\n"

# Write output
outfile = "%s - %s.song" % (title, artist)
outfile = outfile.replace(" ", "_")
with open(outfile, "w") as f:
    f.write(out_text)

# Final check
if delimeter in out_text:
    print("ERROR: A delimeter was not parsed.")
else:
    print("SUCCESS: wrote %s" % (outfile))
