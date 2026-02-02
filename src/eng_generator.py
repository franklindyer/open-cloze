import spacy
import sys

sys.path.append("src")

from registry import GEN_REGISTRY

eng_nlp = spacy.load("en_core_web_md")

def eng_generator(s, snt):
    snt_nlp = eng_nlp(snt)

    puzs = []
    ind = 0
    for tok in snt_nlp:
        tok_total = tok.text + tok.whitespace_
        print(tok.lemma_)
        if tok.is_punct:
            continue
        puzs.append({
            "lemma": tok.lemma_,
            "intervals": f"{ind}-{ind+len(tok.text)}"
        })
        ind += len(tok_total)
    return (s, puzs)

GEN_REGISTRY["eng"] = eng_generator
