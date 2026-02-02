import os

GROUPS = []
LANGS = []
FILES = []

for fname in os.listdir("./data"):
    fpath = os.path.join("data", fname)
    if not os.path.isfile(fpath):
        continue
    FILES.append(fname)

    fparts = fname.split(".")
    if not fparts[0] in GROUPS:
        GROUPS.append(fparts[0])
    if not fparts[1] in LANGS:
        LANGS.append(fparts[1])
