import os
import json
import tqdm
import sys

sys.path.append("src")

from shared import get_conf, tqdm_readlines

CONF = get_conf()
GROUPS = list(CONF["groups"].keys())
LANGS = []
FILES = []

DB_TYPE = sys.argv[1]

import sqlite3
import mysql.connector as con

if DB_TYPE == "mysql":
    cnx = con.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="cloze", charset='utf8mb4')
elif DB_TYPE == "sqlite":
    cnx = sqlite3.connect("db/cloze.sqlite")

cur = cnx.cursor()

def cur_execute(q, args):
    if DB_TYPE == "sqlite":
        q = q.replace("%s", "?")
    cur.execute(q, args) 

GROUP_IDS = []
for grp in GROUPS:
    if len(CONF["groups"][grp]["sentences"]) == 0:
        continue

    cur_execute("INSERT INTO puzzle_groups (label) VALUES (%s)", (grp,))
    GROUP_IDS.append(cur.lastrowid)

    links = set()
    for ln in tqdm_readlines(f"data/{grp}/links.csv"):
        if len(ln) <= 1:
            continue
        ln = ln.strip().split(",")
        id1 = int(ln[0])
        id2 = int(ln[1])
        lnk = (min(id1, id2), max(id1, id2))
        if lnk in links:
            continue
        links.add(lnk)
        cur_execute("INSERT INTO links (group_id, id1, id2) VALUES (%s, %s, %s)", (GROUPS.index(grp)+1, min(id1, id2), max(id1, id2),),)
        cur_execute("INSERT INTO links (group_id, id2, id1) VALUES (%s, %s, %s)", (GROUPS.index(grp)+1, min(id1, id2), max(id1, id2),),)

    for lang in CONF["groups"][grp]["sentences"]:
        for ln in tqdm_readlines(f"data/{grp}/{lang}.tsv"):
            if len(ln) <= 1:
                continue
            ln = ln.strip().split("\t")
            try:
                cur_execute("INSERT INTO sentences (id, lang, group_id, text) VALUES (%s, %s, %s, %s)", (int(ln[0]), lang, GROUP_IDS[GROUPS.index(grp)], ln[1],))
            except:
                print("ERROR ON: " + ln[1])

for grp in GROUPS:
    for lang in CONF["groups"][grp]["puzzles"]: 
        puzs = json.loads(open(f"puzzles/{grp}/{lang}.json").read())
        for lemma in tqdm.tqdm(list(puzs)):
            puzlist = puzs[lemma]
            cur_execute("INSERT OR IGNORE INTO lemmas (lang, text) VALUES (%s, %s)", (lang, lemma,))
            lemma_id = cur.lastrowid
            for puz in puzlist:
                sent_id = int(puz.split(":")[0])
                intervals = puz.split(":")[1]
                cur_execute("INSERT OR IGNORE INTO puzzles (sentence_id, group_id, lemma_id, intervals) VALUES (%s, %s, %s, %s)", (sent_id, GROUP_IDS[GROUPS.index(grp)], lemma_id, intervals,))

cnx.commit()

cur.close()
cnx.close()
