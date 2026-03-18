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

cnx.execute("""
    UPDATE sentences SET keep=1 WHERE EXISTS (
        SELECT * FROM puzzles WHERE sentence_id=sentences.id
    )
""")

cnx.execute("""
    UPDATE sentences SET keep=1 WHERE EXISTS (
        SELECT * FROM links INNER JOIN sentences AS sentences2
        ON links.id1 = sentences2.id
        WHERE links.id2 = sentences.id1
            AND sentences2.keep = 1  
    )
""")

cnx.execute("DELETE FROM sentences WHERE keep = 0")

t1_tot = cnx.execute("SELECT COUNT(*) FROM sentences").fetchone()[0]

cnx.commit()
cur.close()
cnx.close()

print(f"Number of sentences decreased {t0_tot} -> {t1_tot}")
