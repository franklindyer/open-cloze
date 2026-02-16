import datetime
import json
import os
import re
import mysql.connector as sql
from multiprocessing.pool import ThreadPool

from flask import Flask, abort, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DB_READ_POOL = ThreadPool(processes=10)

def unpool_query(con, q, args):
    cur = con.cursor()
    cur.execute(q, args) 
    res = cur.fetchall()
    cur.close()
    return list(res)

def pool_query(con, q, args=()):
    res = DB_READ_POOL.apply(unpool_query, (con, q, args,))
    return res

SQL_CON = sql.connect(host="mysql", port=3306, user="root", passwd="root", db="cloze", charset="utf8mb4") 

cur = SQL_CON.cursor()
cur.execute("SELECT label FROM puzzle_groups")
all_groups = [r[0] for r in cur.fetchall()]
print(all_groups, flush=True)
cur.close()

def get_random_verbatim_cloze(con, src_langs, tgt_lang, v_str, n=1, groups=all_groups):
    lang_params = ','.join(["%s"] * len(src_langs))
    group_params = ','.join(["%s"] * len(groups))
    ress = pool_query(con, f"""
        SELECT gid, src_txt, tgt_txt, grp FROM (
            SELECT sents_tgt.group_id AS gid, sents_src.text AS src_txt, sents_tgt.text AS tgt_txt, puzzle_groups.label AS grp
            FROM sentences AS sents_tgt 
            INNER JOIN links AS links ON sents_tgt.id=links.id1
            INNER JOIN sentences AS sents_src ON sents_src.id=links.id2 
            INNER JOIN puzzle_groups AS puzzle_groups ON sents_tgt.group_id=puzzle_groups.id
            WHERE sents_tgt.text LIKE %s 
                AND sents_tgt.lang=%s
                AND sents_src.lang IN ({lang_params})
                AND puzzle_groups.label IN ({group_params})
                AND sents_src.group_id = sents_tgt.group_id
        ) AS tableAlias
#        ORDER BY RAND()
        LIMIT %s
    """, (f"%{v_str}%", tgt_lang,) + tuple(src_langs) + tuple(groups) + (n,))
    if len(ress) == 0:
        return None
    for i in range(len(ress)):
        m = re.search(v_str, ress[i][2], re.IGNORECASE)
        ress[i] = ress[i] + (f"{m.start()}-{m.end()}",)
    return [{
        "id": None,
        "word": v_str,
        "blanks": res[4],
        "source": res[1],
        "target": res[2],
        "group": res[3]
    } for res in ress]

def get_random_cloze(con, src_langs, tgt_lang, lemma, n=1, groups=all_groups):
    lang_params = ','.join(["%s"] * len(src_langs))
    group_params = ','.join(["%s"] * len(groups))
    ress = pool_query(con, f"""
        SELECT pid, intervals, src_txt, tgt_txt, grp FROM (
            SELECT puzzles.id AS pid, puzzles.group_id AS gid, puzzles.intervals AS intervals, sents_src.text AS src_txt, sents_tgt.text AS tgt_txt, puzzle_groups.label AS grp
            FROM puzzles AS puzzles
            INNER JOIN lemmas AS lemmas ON puzzles.lemma_id=lemmas.id
            INNER JOIN sentences AS sents_tgt ON puzzles.sentence_id=sents_tgt.id
            INNER JOIN links AS links ON puzzles.sentence_id=links.id1
            INNER JOIN sentences AS sents_src ON sents_src.id=links.id2 
            INNER JOIN puzzle_groups AS puzzle_groups ON sents_tgt.group_id=puzzle_groups.id
            WHERE lemmas.text=%s 
                AND sents_tgt.lang=%s
                AND sents_src.lang IN ({lang_params})
                AND puzzle_groups.label IN ({group_params})
                AND puzzles.group_id = sents_src.group_id
                AND sents_src.group_id = sents_tgt.group_id
        ) AS tableAlias
        ORDER BY RAND()
        LIMIT %s
    """, (lemma, tgt_lang,) + tuple(src_langs) + tuple(groups) + (n,))
    if len(ress) == 0:
        return None
    return [{
        "id": res[0],
        "word": lemma,
        "blanks": res[1],
        "source": res[2],
        "target": res[3],
        "group": res[4]
    } for res in ress]

def add_blanks(puz):
    bls = [bl.split('-') for bl in puz['blanks'].split(",")]
    bls = [(int(bl[0]), int(bl[1])) for bl in bls][::-1]
    pt = puz['target']
    for bl in bls:
        pt = pt[:bl[0]] + "{{" + pt[bl[0]:bl[1]] + "}}" + pt[bl[1]:]
    puz['puzzle'] = pt
    return puz

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/status")
@cross_origin()
def get_status():
    # j = request.json
    return {}

@app.route("/cloze")
@cross_origin()
def get_cloze():
    src_langs = request.args.get("srcs").split(',')
    tgt_lang = request.args.get("tgt")
    lemma = request.args.get("lemma")
    groups = request.args.get("groups")
    if groups is None or len(groups) == 0:
        groups = all_groups
    else:
        groups = groups.split(',')
    n_results = min(int(request.args.get("n")), 10)
    
    cloze = None
    if lemma[0] == '"' and lemma[-1] == '"':
        print(lemma, flush=True)
        cloze = get_random_verbatim_cloze(SQL_CON, src_langs, tgt_lang, lemma[1:-1], n=n_results, groups=groups)
    else:
        cloze = get_random_cloze(SQL_CON, src_langs, tgt_lang, lemma, n=n_results, groups=groups)
    if cloze == None:
        abort(404)

    cloze = [add_blanks(puz) for puz in cloze]
    response = jsonify(cloze)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

from waitress import serve
serve(app, host="0.0.0.0", port=8080)
