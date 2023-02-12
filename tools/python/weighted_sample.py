from __future__ import print_function

import numpy as np
import random
import sys

from tqdm import tqdm


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: {} <bigram_file> <sample_size>'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(0)

    bigram_file, sample_size = sys.argv[1], int(sys.argv[2])
    weights = []
    for line in tqdm(open(bigram_file), 'read input'):
        _, count = line.split('\t', 1)
        weights.append(int(count))

    prob = np.array(weights, dtype=np.float64)
    prob /= prob.sum()

    sample = set(np.random.choice(prob.size, sample_size, replace=False, p=prob))
    for i, line in tqdm(enumerate(open(bigram_file)), 'generate output'):
        if i in sample:
            print(line, end='')
