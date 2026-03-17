from collections import Counter
import numpy as np
import random
import spacy
from spacy.matcher import DependencyMatcher
from spacy.displacy import parse_deps
import sys

sys.path.append("src")

from registry import GEN_REGISTRY
# from shared import lines_set

# deu_nlp = spacy.load("de_core_news_md")
deu_nlp = spacy.load("de_zdl_lg")
# deu_nlp = spacy.load("de_zdl_dist")

def deu_generator():
    TARGET_NUM = 20
    REDUCED_PROB = 0.2
    MAX_NUM = 50

    def gen(s, snt):
        if not "counts" in s:
            s["counts"] = Counter()

        snt_nlp = deu_nlp(snt)

        def search_nlp(nlp, ptn):
            matcher = DependencyMatcher(nlp.vocab)
            matcher.add("PTN", [ptn])
            return matcher

        # Matcher for auxiliary prepositions
        auxp_match = search_nlp(deu_nlp, [{
                "RIGHT_ID": "anchor", 
                "RIGHT_ATTRS": { "POS": "VERB" }
            }, {
                "LEFT_ID": "anchor", 
                "REL_OP": ">", 
                "RIGHT_ID": "obl_obj", 
                "RIGHT_ATTRS": {
                    "POS": "NOUN",
                    "DEP": "obl"
                }
            }, {
                "LEFT_ID": "obl_obj", 
                "REL_OP": ">", 
                "RIGHT_ID": "obl_prep", 
                "RIGHT_ATTRS": {
                    "POS": "ADP",
                    "DEP": "case"
            }
        }])

        # Get all separable verb prefixes, reflexive pronouns and aux prepositions
        svp_map = {}
        svp_positions = set()
        refl_map = {}
        auxp_map = {}        
        for dep in parse_deps(snt_nlp)["arcs"]:
            if dep["label"] == "svp":
                svp_map[dep["start"]] = dep["end"]
                svp_positions.add(dep["start"])
                svp_positions.add(dep["end"])
            elif dep["label"] == "expl:pv":
                vp_inds = (dep["start"], dep["end"])
                if dep["dir"] == "left":
                    vp_inds = (vp_inds[1], vp_inds[0]) 
                refl_map[vp_inds[0]] = vp_inds[1]                
            ## elip dep["label"] == ""

        auxp_matches = auxp_match(snt_nlp)
        for m in auxp_matches:
            auxp_map[m[1][0]] = m[1][2]

        tok_positions = np.cumsum([0] + [len(tok.text) + len(tok.whitespace_) for tok in snt_nlp])

        puzs = []
        last_len = 0
        for (tok_num, tok) in zip(range(len(snt_nlp)), snt_nlp):
            if tok.is_punct:
                continue
            if any(c in "0123456789" for c in tok.lemma_):
                continue

            lemma = tok.lemma_
            is_separable = False
            if tok_num in svp_map:
                lemma = snt_nlp[svp_map[tok_num]].lemma_ + lemma
                is_separable = True
            elif tok_num in svp_positions:
                continue

            if s["counts"][lemma] >= MAX_NUM:
                continue
            elif s["counts"][lemma] >= TARGET_NUM and random.random() < REDUCED_PROB:
                continue

            tok_combos = []
            if not is_separable:
                tok_combos.append((lemma, [tok_num]))
            else:
                tok_combos.append((lemma, [tok_num, svp_map[tok_num]])) 
            if tok_num in refl_map:
                tok_combos.append(("sich " + lemma, tok_combos[0][1] + [refl_map[tok_num]]))
            if tok_num in auxp_map:
                p = snt_nlp[auxp_map[tok_num]].lemma_
                tok_combos.append((tok_combos[-1][0] + " " + p, tok_combos[-1][1] + [auxp_map[tok_num]]))

            for combo in tok_combos:
                lemma, combo_inds = combo
                sorted(combo_inds)
                 
                s["counts"][lemma] += 1 

                puzs.append({
                    "lemma": lemma,
                    "intervals": ",".join([str(tok_positions[tn]) + "-" + str(tok_positions[tn] + len(snt_nlp[tn].text)) for tn in combo_inds])
                })

            #s["counts"][lemma] += 1
            #if is_separable:
            #    i1 = tok_positions[tok_num]
            #    i2 = i1 + len(tok.text)
            #    i3 = tok_positions[svp_map[tok_num]]
            #    i4 = i3 + len(snt_nlp[svp_map[tok_num]].text) 
            #    puzs.append({
            #        "lemma": lemma,
            #        "intervals": f"{i1}-{i2},{i3}-{i4}" 
            #    })
            #else:
            #    i1 = tok_positions[tok_num]
            #    i2 = tok_positions[tok_num] + len(tok.text)
            #    puzs.append({
            #        "lemma": lemma,
            #        "intervals": f"{i1}-{i2}"
            #    })
        return (s, puzs)
    return gen

GEN_REGISTRY["deu"] = deu_generator()
