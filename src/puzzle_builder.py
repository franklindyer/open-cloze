import json
import spacy
import sys
import tqdm

sys.path.append("src")

from shared import get_conf, tqdm_readlines
from registry import GEN_REGISTRY

import generators
import deu_generator

# A puzzle generator for a language L should be a function that takes a state object
#   and a sentence in that language and returns a new state object plus a list of puzzles.
#   A puzzle takes the form of a lemma plus a set of (comma-separated) intervals.

# MAX_PER_GROUP = 1000
MAX_PER_GROUP = None

def gen_puzzles(group, lang):
    s = {}  # State object
    gen = GEN_REGISTRY[lang]
    fname = f"data/{group}/{lang}.tsv"
   
    all_puz = {}

    included_ids = []
    for ln in tqdm_readlines(fname, max=MAX_PER_GROUP):
        if len(ln) <= 1:
            continue
        r = ln.strip().split("\t")
        id = int(r[0])
        s, puzs = gen(s, r[1])
        if len(puzs) > 0:
            included_ids.append(id)
        for puz in puzs:
            lemma = puz["lemma"]
            if not lemma in all_puz:
                all_puz[lemma] = []
            all_puz[lemma].append(str(id) + ":" + puz["intervals"])

#    with open(f"puzzles/{group}/{lang}_ids.txt", "w") as f:
#        for id in included_ids:
#            f.write(f"{id}\n")

    with open(f"puzzles/{group}/{lang}.json", "w") as f:
        f.write(json.dumps(all_puz, indent=4, ensure_ascii=False))

    return all_puz

def gen_all_puzzles():
    CONF = get_conf()
    for grp in CONF["groups"]:
        for lang in CONF["groups"][grp]["puzzles"]:
            gen_puzzles(grp, lang)

gen_all_puzzles()
