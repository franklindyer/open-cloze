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

import mysql.connector as con

cnx = con.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="cloze")
cur = cnx.cursor()

for lang in LANGS:
    cur.execute("INSERT INTO langs (iso3) VALUES (%s)", (lang,))

for grp in GROUPS:
    cur.execute("INSERT INTO puzzle_groups (label) VALUES (%s)", (grp,))

for fname in FILES:
    fparts = fname.split(".")
    fpath = os.path.join("data", fname)
    group = fparts[0]
    lang = fparts[1]

    if fparts[2] == "txt":
        i = 0
        for ln in open(fpath).readlines():
            if len(ln) <= 1:
                continue
            ln = ln.strip()
            cur.execute("INSERT INTO sentences (position, group_id, lang_id, text) VALUES (%s, %s, %s, %s)", (i, LANGS.index(lang)+1, GROUPS.index(group)+1, ln,))
            i += 1

cur.close()
cnx.close()
