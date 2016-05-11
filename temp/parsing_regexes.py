from pprint import pprint
import ast
import re

FOLLOW = "../songs/production/i_will_follow_you_into_the_dark-death_cab_for_cutie.song"
BAD_MOON = "../songs/production/bad_moon_rising-credence_clearwater_revival.song"

sections = []
metadata = {}
cur = None
with open(BAD_MOON, "r") as f:
    text = f.read()
for line in text.splitlines():
    # strip initial white space
    line = line.rstrip()
    # ignore blank lines
    if not line: continue
    # identify line type statements (ie "chorus:")
    if line == line.lstrip():
        cur = []
        sections.append((line.strip(":"), cur))
    # work with all remaining lines (content)
    else:
        cur.append(line.strip())

if sections[0][0] == "header":
    for line in sections.pop(0)[1]:
        key, value = line.split('=', 1)
        metadata[key] = ast.literal_eval(value.strip())

pprint(metadata)
pprint(sections)
