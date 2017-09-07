import argparse
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import sh

from StringIO import StringIO


def convert_to_data_frame(iterable):
    df = pd.read_table(iterable, names=('metric', 'qid', 'value'), sep=r'\s+')
    return df.pivot(index='qid', columns='metric', values='value')


def run_trec_eval(qrels, run_files, trec_eval):
    for run in run_files:
        result = trec_eval(qrels, run)
        df = convert_to_data_frame(StringIO(result))
        df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
        yield run, df


def get_rows(results, metrics, nbaselines=1):
    baselines = []
    for i, result in enumerate(results):
        run, df = result
        values = list(df.loc['all'][metrics])
        pvalues_list = []

        for baseline in baselines:
            pvalues = []
            for m in metrics:
                x = np.array(baseline.drop('all')[m])
                y = np.array(df.drop('all')[m])
                _, pvalue = stats.ttest_rel(x, y)
                pvalues.append(pvalue)
            pvalues_list.append(pvalues)

        if nbaselines > 0:
            if len(pvalues_list) < nbaselines:
                pvalues_list.extend([len(values) * [np.nan]] * (nbaselines - len(pvalues_list)))
        else:
            pvalues_list.extend([len(values) * [np.nan]])

        yield run, values, zip(*pvalues_list)

        if i < nbaselines:
            baselines.append(df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--measure', dest='m', action='append')
    parser.add_argument('-c', '--complete_rel_info_wanted', dest='c', action='store_true')
    parser.add_argument('-l', '--level_for_rel', dest='l', type=int)
    parser.add_argument('-N', '--Number_docs_in_coll', dest='N', type=int)
    parser.add_argument('-M', '-Max_retrieved_per_topic', dest='M', type=int)

    parser.add_argument('-b', dest='nbaselines', type=int, default=0,
                        help='number of baselines (default: %(default)s)')
    parser.add_argument('--tabulate', action='store_true',
                        help='use tabulate to generate LaTeX tabular output')
    parser.add_argument('--precision', type=int, default=4,
                        help='float precision width (default: %(default)s)')
    parser.add_argument('--show-pvalues', action='store_true',
                        help='show p-values')
    parser.add_argument('qrels')
    parser.add_argument('run_files', metavar='run_file', nargs='+')
    args = parser.parse_args()

    short_forms = {'ndcg': 'NDCG',
                   'ndcg_cut_5': 'N@5',
                   'ndcg_cut_10': 'N@10',
                   'ndcg_cut_20': 'N@20',
                   'P_5': 'P@5',
                   'P_10': 'P@10',
                   'P_20': 'P@20',
                   'recip_rank': 'MRR',
                   'map': 'MAP'}

    metrics = ['ndcg_cut_5', 'ndcg_cut_10', 'ndcg_cut_20', 'P_5', 'P_10', 'P_20', 'recip_rank', 'map']

    marks = [('**', '*'), ('++', '+'), ('!!', '!')]

    def to_marks(pvalues):
        result = ''
        for i, p in enumerate(pvalues):
            doublestar, star = marks[i]
            if not np.isnan(p):
                if p < 0.01:
                    result += doublestar
                elif p < 0.05:
                    result += star
        if args.show_pvalues:
            return '{} ({:.4f})'.format(result, p)
        else:
            return '{}'.format(result, p)

    trec_eval_opts = ['-q', '-m', 'all_trec']
    if args.c:
        trec_eval_opts.append('-c')
    if args.l is not None:
        trec_eval_opts.extend(['-l', args.l])
    if args.N is not None:
        trec_eval_opts.extend(['-N', args.N])
    if args.M is not None:
        trec_eval_opts.extend(['-M', args.M])
    trec_eval = sh.trec_eval.bake(trec_eval_opts)

    results = run_trec_eval(args.qrels, args.run_files, trec_eval)

    header_template = '{:<' + str(args.precision + 2 + args.nbaselines * 2) + 's}  '
    template = '{:<0.' + str(args.precision) + 'f}{:<' + str(args.nbaselines * 2) + 's}  '

    if args.tabulate:
        from tabulate import tabulate
        table = []
        table.append(['Run'] + [short_forms.get(m, m) for m in metrics])
        for run, values, pvalues in get_rows(results, metrics, nbaselines=args.nbaselines):
            stars = map(to_marks, pvalues)
            table.append([run] + [template.format(v, m) for v, m in zip(values, stars)])
        print tabulate(table, tablefmt='latex')
    else:
        print ''.join([header_template.format(short_forms.get(m, m)) for m in metrics] + ['NAME'])
        for run, values, pvalues in get_rows(results, metrics, nbaselines=args.nbaselines):
            stars = map(to_marks, pvalues)
            print ''.join([template.format(v, m) for v, m in zip(values, stars)] + [run])
