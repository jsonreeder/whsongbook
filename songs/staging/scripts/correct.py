import os
query = """intro:
    [|"""

for song in os.listdir("../production"):
    with open("../production/" + song, "r") as f:
        file = f.read()
        if query in file:
            print(file.splitlines()[1])
