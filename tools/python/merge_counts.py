from __future__ import print_function

import fileinput
import itertools


def parse_input():
    for line in fileinput.input():
        yield line.strip().split(None, 2)


for k, grp in itertools.groupby(parse_input(), key=lambda x: x[:2]):
    c = sum(int(x[2]) for x in grp)
    print('{} {}\t{}'.format(k[0], k[1], c))
