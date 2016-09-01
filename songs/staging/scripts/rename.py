import sys
import os

def extract_name(input_file):
    with open(input_file, "r") as f:
        lines = f.read().splitlines()

    title = lines[1][13:-1]
    artist = lines[2][14:-1]

    return(title, artist)

def create_new(input_file):
    title, artist = extract_name(input_file)
    formatted = "%s - %s.song" % (title, artist)
    formatted = formatted.replace(" ", "_")
    with open (input_file, "r") as f:
        lines = f.read().splitlines()
    with open(formatted, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    create_new(sys.argv[1])
    os.remove(sys.argv[1])
