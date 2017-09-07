from __future__ import print_function

import argparse
import os.path
import pandas as pd


def extract_name(path):
    fname = os.path.basename(path)
    return fname.split('.', 1)[1]


def parse_fields(text):
    if text == 'full_index':
        return text, 0
    else:
        name, ratio = text.rsplit('_', 1)
        return name, float(ratio)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('eval_table')
    parser.add_argument('gini_table')
    parser.add_argument('timing_table')
    args = parser.parse_args()

    # eval.table
    df1 = pd.read_table(args.eval_table, sep=r'\s+')
    df1.columns = [name.lower() for name in df1.columns]
    df1.name = df1.name.apply(extract_name)
    df1['p_method'], df1['p_ratio'] = df1.name.apply(parse_fields).str

    # gini.table & timing.table
    df2 = pd.read_table(args.gini_table, sep=r'\s+')
    df2.name = df2.name.apply(extract_name)

    df3 = pd.read_table(args.timing_table, sep=r'\s+')
    df3.name = df3.name.apply(extract_name)

    df = reduce(lambda a, b: pd.merge(a, b, on='name'), [df1, df2, df3])
    csv_output = df.to_csv(None)
    print(csv_output, end='')
