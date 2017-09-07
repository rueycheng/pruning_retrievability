from __future__ import print_function

import fileinput

from tqdm import tqdm


for line in tqdm(fileinput.input(), desc='Read input'):
    g1, g2, count = line.strip().split()
    if len(g1) < 3 or len(g1) > 20 or len(g2) < 3 or len(g2) > 20:
        continue
    if not g1.isalpha() or not g2.isalpha():
        continue
    count = int(count)
    if count < 10:
        continue
    print(line, end='')
