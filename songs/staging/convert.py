# Initialize gloabls
infile = "junk_in.txt"
outfile = "junk_out.txt"
out_text = ""
delimeter = "\\"

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

            # Parse chords
            if delimeter in str(content):
                new_content = []
                i = 0
                while i < len(content) - 1:
                    chord_line = content[i]
                    lyric_line = content[i+1]
                    if delimeter in lyric_line:
                        chords = chord_line.split()
                        lyrics = lyric_line
                        while len(chords) > 0:
                            chord = chords.pop(0)
                            lyrics = lyrics.replace(delimeter, "[%s]" % (chord), 1)

                    # Throw error if chords are not placed
                    # if len(chords) > 0:
                    #     print("ERROR: Chords (%s) have not been placed" % str(chords))

                    # Throw error if delimeter remains in line

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
# with open(outfile, "w") as f:
    # for p in parts:
    #     line = str(p) + "\n\n"
    #     f.write(line)

print(out_text)
