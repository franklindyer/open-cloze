from collections import Counter
import random
import spacy
import sys

sys.path.append("src")

from registry import GEN_REGISTRY

eng_nlp = spacy.load("en_core_web_md")
spa_nlp = spacy.load("es_core_news_md")
rus_nlp = spacy.load("ru_core_news_md")

def simple_generator(nlp):
    TARGET_NUM = 20
    REDUCED_PROB = 0.2
    MAX_NUM = 50

    def gen(s, snt):
        if not "counts" in s:
            s["counts"] = Counter()

        snt_nlp = nlp(snt)

        puzs = []
        ind = 0
        for tok in snt_nlp:
            tok_total = tok.text + tok.whitespace_
            if tok.is_punct:
                continue
            if any(c in "0123456789" for c in tok.lemma_):
                continue
            lemma = tok.lemma_

            if s["counts"][lemma] >= MAX_NUM:
                continue
            elif s["counts"][lemma] >= TARGET_NUM and random.random() < REDUCED_PROB:
                continue

            s["counts"][lemma] += 1
            puzs.append({
                "lemma": lemma,
                "intervals": f"{ind}-{ind+len(tok.text)}"
            })
            ind += len(tok_total)
        return (s, puzs)
    return gen

GEN_REGISTRY["eng"] = simple_generator(eng_nlp)
GEN_REGISTRY["spa"] = simple_generator(spa_nlp)
GEN_REGISTRY["rus"] = simple_generator(rus_nlp)
