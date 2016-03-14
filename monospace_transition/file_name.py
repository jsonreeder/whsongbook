import sys

def file_name(input_string):
    """Take the first two lines from a song and return a file name
       in the preferred format."""

    lines = [l for l in input_string.splitlines()]
    output_string = ""
    for i, item in enumerate(lines):
        underscores = item.replace(" ", "_")
        output_string += underscores
        if i < len(lines) - 1:
            output_string += "-"
    output_string += ".txt"
    output_string = output_string.lower()

    return output_string

if __name__ == "__main__":
    file_name = file_name(sys.argv[1])
    print(file_name)


