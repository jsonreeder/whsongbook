# Initialize globals
outfile = "temp_out.song"

# Define heper funcions
def parse_header(text):
    return text

def run():
    with open("junk_processing.txt", "r") as f:
        text = f.read()

        out_text = parse_header(text)

        with open(outfile, "w") as o:
            o.write(out_text)

# Run
run()
