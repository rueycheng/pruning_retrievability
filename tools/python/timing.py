from __future__ import print_function

import sys


print('name time')
for fname in sys.argv[1:]:
    sec = float(list(open(fname))[0].strip())
    print(fname, sec)
