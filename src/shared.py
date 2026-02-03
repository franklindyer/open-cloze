import json
import os
import tqdm

def get_conf():
    return json.loads(open("conf.json").read())

def tqdm_readlines(fname):
    with open(fname, "rb") as f:
        num_lines = sum(1 for _ in f.readlines())
    return tqdm.tqdm(open(fname).readlines(), total=num_lines)

def lines_set(fname):
    return set([ln.strip() for ln in open(f"resources/{fname}").readlines() if len(ln) > 1])
