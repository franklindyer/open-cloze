import os
import json
import tqdm
import sys

sys.path.append("src")

from shared import get_conf, tqdm_readlines

import sqlite3
import mysql.connector as con

cnx = sqlite3.connect("db/cloze.sqlite")

t0_tot = cnx.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]
print(f"Total num sentences: {t0_tot}")

print("Marking used sentences to KEEP...")
cnx.execute("""
    UPDATE sentences SET keep=1 WHERE EXISTS (
        SELECT * FROM puzzles WHERE sentence_id=sentences.id
    )
""")
cnx.commit()

print("Deleting links not attached to at least one sentence marked KEEP...")
cnx.execute("""
    DELETE FROM links WHERE rowid NOT IN (
        SELECT links.rowid FROM links
        INNER JOIN sentences AS s1 ON s1.id = links.id1
        INNER JOIN sentences AS s2 on s2.id = links.id2
        WHERE s1.keep=1 OR s2.keep=1
    )
""")
cnx.commit()

print("Marking links to used sentences to KEEP...")
cnx.execute("""
    UPDATE sentences SET keep=1 WHERE id IN (
        SELECT id1 FROM links 
    )
""")
cnx.commit()

print("Deleting sentences not flagged to KEEP...")
cnx.execute("DELETE FROM sentences WHERE keep = 0")
cnx.commit()

print("Vacuuming database...")
cnx.execute("VACUUM")
cnx.commit()

t1_tot = cnx.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]

# cur.close()
cnx.close()

print(f"Number of sentences decreased {t0_tot} -> {t1_tot}")
