import argparse
import pandas as pd

from smart_open import smart_open


def gini(arr):
    values = arr.sort_values()
    area = values.cumsum().sum()
    fair_area = values.sum() * df.size / 2.0
    # height, area = 0, 0
    # for value in arr.sort_values():
    #     height += value
    #     area += (height - value) / 2.0
    # fair_area = height * df.size / 2.0
    return (fair_area - area) / fair_area


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='append')
    parser.add_argument('ret_files', metavar='ret_file', nargs='+')
    args = parser.parse_args()

    column_names = ['cm_10', 'cm_20', 'cm_50', 'cm_100', 'gm_0.5', 'gm_1.0', 'gm_1.5', 'gm_2.0']

    print 'name', 'measure', 'r_sum', 'n_docs', 'gini'
    for fname in args.ret_files:
        df = pd.read_table(smart_open(fname), skiprows=1, header=None, sep=' ',
                           usecols=xrange(1, 9), names=column_names)
        columns = args.f if args.f else df.columns
        for col in columns:
            g = gini(df[col])
            print fname, df[col].name, df[col].sum(), df.size, g
