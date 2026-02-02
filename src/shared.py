import os
import tqdm

def tqdm_readlines(fname):
    with open(fname, "rb") as f:
        num_lines = sum(1 for _ in f.readlines())
    return tqdm.tqdm(open(fname).readlines(), total=num_lines)

