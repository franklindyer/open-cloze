import os
import tqdm
import sys

sys.path.append("src")

from shared import tqdm_readlines

ENABLED_GROUPS = ["tatoeba"]
GROUPS = []
LANGS = []
FILES = []

GROUP_LANG_PAIRS = []

for fname in os.listdir("./puzzles"):
    fpath = os.path.join("puzzles", fname)
    if not os.path.isfile(fpath):
        continue
    FILES.append(fname)

    fparts = fname.split(".")
    if fparts[2] == "json" and fparts[0] in ENABLED_GROUPS:
        GROUP_LANG_PAIRS.append((fparts[0], fparts[1]))

GROUPS = list(set([x[0] for x in GROUP_LANG_PAIRS]))

import mysql.connector as con

cnx = con.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="cloze", charset='utf8mb4')
cur = cnx.cursor()

GROUP_IDS = []
for grp in GROUPS:
    cur.execute("INSERT INTO puzzle_groups (label) VALUES (%s)", (grp,))
    GROUP_IDS.append(cur.lastrowid)

    for ln in tqdm_readlines(f"data/{grp}/links.csv"):
        if len(ln) <= 1:
            continue
        ln = ln.strip().split(",")
        id1 = int(ln[0])
        id2 = int(ln[1])
        cur.execute("INSERT INTO links (group_id, id1, id2) VALUES (%s, %s, %s)", (GROUPS.index(grp)+1, min(id1, id2), max(id1, id2),),)

    for (grp2, lang) in GROUP_LANG_PAIRS:
        if grp2 != grp:
            continue
        for ln in tqdm_readlines(f"data/{grp}/{lang}.tsv"):
            if len(ln) <= 1:
                continue
            ln = ln.strip().split("\t")
            try:
                cur.execute("INSERT INTO sentences (id, lang, group_id, text) VALUES (%s, %s, %s, %s)", (int(ln[0]), lang, GROUP_IDS[GROUPS.index(grp)], ln[1],))
            except:
                print("ERROR ON: " + ln[1])

for (grp, lang) in GROUP_LANG_PAIRS:
    continue

cnx.commit()

cur.close()
cnx.close()
