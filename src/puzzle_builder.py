import json
import spacy
import sys
import tqdm

sys.path.append("src")

from shared import tqdm_readlines
from registry import GEN_REGISTRY

import eng_generator

# A puzzle generator for a language L should be a function that takes a state object
#   and a sentence in that language and returns a new state object plus a list of puzzles.
#   A puzzle takes the form of a lemma plus a set of (comma-separated) intervals.

def gen_puzzles(group, lang):
    s = {}  # State object
    gen = GEN_REGISTRY[lang]
    fname = f"data/{group}/{lang}.tsv"
   
    all_puz = {}

    for ln in tqdm_readlines(fname):
        if len(ln) <= 1:
            continue
        r = ln.strip().split("\t")
        id = int(r[0])
        s, puzs = gen(s, r[1])
        for puz in puzs:
            lemma = puz["lemma"]
            if not lemma in all_puz:
                all_puz[lemma] = []
            all_puz[lemma].append(str(id) + ":" + puz["intervals"])

    with open(f"puzzles/{group}.{lang}.json", "w") as f:
        f.write(json.dumps(all_puz, indent=4))

    return all_puz

gen_puzzles("test", "eng")
