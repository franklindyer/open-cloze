import spacy
from spacy.matcher import DependencyMatcher
import sys

sys.path.append("./src")

from shared import tqdm_readlines 

deu_nlp = spacy.load("de_zdl_lg")

matcher = DependencyMatcher(deu_nlp.vocab)

snts = [deu_nlp(ln.strip().split("\t")[1]) for (ln, _) in zip(tqdm_readlines("data/tatoeba/deu.tsv"), range(1000))]
