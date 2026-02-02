import os
import tqdm
import sys

sys.path.append("src")

from shared import tqdm_readlines

GROUPS = []
LANGS = []
FILES = []

for fname in os.listdir("./puzzles"):
    fpath = os.path.join("puzzles", fname)
    if not os.path.isfile(fpath):
        continue
    FILES.append(fname)

    fparts = fname.split(".")
    if not fparts[0] in GROUPS:
        GROUPS.append(fparts[0])
    if not fparts[1] in LANGS and fparts[1] != "links":
        LANGS.append(fparts[1])

import mysql.connector as con

cnx = con.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="cloze")
cur = cnx.cursor()

GROUP_IDS = []
for grp in GROUPS:
    cur.execute("INSERT INTO puzzle_groups (label) VALUES (%s)", (grp,))
    GROUP_IDS.append(cur.lastrowid)

for fname in FILES:
    fparts = fname.split(".")
    fpath = os.path.join("puzzles", fname)
    group = fparts[0]
    lang = fparts[1]

    if lang == "links":
        for ln in tqdm_readlines(fpath):
            if len(ln) <= 1:
                continue
            ln = ln.strip().split(",")
            id1 = int(ln[0])
            id2 = int(ln[1])
            cur.execute("INSERT INTO links (group_id, id1, id2) VALUES (%s, %s, %s)", (GROUPS.index(group)+1, min(id1, id2), max(id1, id2),),)
    elif fparts[2] == "txt":
        i = 0
        for ln in tqdm_readlines(fpath):
            if len(ln) <= 1:
                continue
            ln = ln.strip().split("\t")
            cur.execute("INSERT INTO sentences (id, lang, group_id, text) VALUES (%s, %s, %s, %s)", (int(ln[0]), lang, GROUP_IDS[GROUPS.index(group)], ln[1],))
            i += 1

cnx.commit()

cur.close()
cnx.close()
