import argparse
import os
import sh
import string
import sys
import tempfile
import time

from more_itertools import chunked
from tqdm import tqdm
from smart_open import smart_open


def make_indri_term_trans():
    ascii_chars = set(map(chr, range(0x00, 0x80)))
    mask = ''.join(ascii_chars - set(string.letters) - set(string.digits))
    return string.maketrans(mask, ' ' * len(mask))


def parse_components(iterable):
    """Parse result entries from run output"""
    for line in iterable:
        if line.startswith('#') or line.startswith('\t'):
            print >>sys.stderr, line,
            continue
        qid, _, docno, _, sim, _ = line.split()
        yield {'qid': int(qid), 'docno': docno, 'score': float(sim)}


def run_batched_queries(texts, index_path, outfile, timings_file, k=10, threads=1, batch_size=1000, rule='method:lm'):
    """Run queries in batches against an Indri index

    Args:
        texts: a sequence of input texts
        index_path: path to the Indri index
        outfile: output filename
        timings_file: file to store the timing result
        k: number of docs to retrieve
        threads: number of threads to use
        batch_size: number of queries in a batch
    """
    assert texts
    assert os.path.exists(index_path)
    assert k > 0

    indri_term_trans = make_indri_term_trans()

    n_texts = len(texts)
    n_batches = n_texts / batch_size + int(n_texts % batch_size > 0)
    seen_docs = set()

    tbar = tqdm(chunked(enumerate(texts, 1), batch_size),
                desc='run batched queries',
                total=n_batches)

    run_output = smart_open(outfile, 'wb')

    start_t = time.time()
    for batch in tbar:
        with tempfile.NamedTemporaryFile(delete=True) as out:
            out.write('<parameters>\n')
            for qid, text in batch:
                ascii_text = text.encode('ascii', errors='replace').replace('?', ' ').lower()
                terms = ascii_text.translate(indri_term_trans).split()
                if not terms:
                    continue
                query = '#combine({})'.format(' '.join(terms))
                out.write(
                    '  <query>\n'
                    '    <number>{qid}</number>\n'
                    '    <text>{query}</text>\n'
                    '  </query>\n'
                    .format(qid=qid, query=query)
                )
            out.write('</parameters>\n')
            out.flush()

            runs_input = sh.IndriRunQuery('-index={}'.format(index_path),
                                          '-count={}'.format(k),
                                          '-threads={}'.format(threads),
                                          '-rule={}'.format(rule),
                                          '-trecFormat=1',
                                          out.name,
                                          _iter=True)
            lines = list(runs_input)
            run_output.writelines(lines)
            for entry in parse_components(lines):
                seen_docs.add(entry['docno'])
        tbar.set_description('run batched queries (got: {} docs)'.format(len(seen_docs)))

    elapsed = time.time() - start_t
    if timings_file is not None:
        with open(timings_file, 'wb') as timings_out:
            timings_out.write('{}\n'.format(elapsed))
    print 'run saved to {} in {} seconds'.format(outfile, elapsed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=int,
                        help='number of docs to retrieve for each query')
    parser.add_argument('-threads', type=int,
                        help='number of threads to use')
    parser.add_argument('-batch-size', metavar='B', type=int,
                        help='batch size')
    parser.add_argument('-rule',
                        help='retrieval model (via IndriRunQuery option -rule=RULE)')
    parser.add_argument('bigram_file')
    parser.add_argument('index_path')
    parser.add_argument('output_file')
    parser.add_argument('timings_file', nargs='?')
    parser.set_defaults(k=10, threads=1, batch_size=1000, rule='method:lm')
    args = parser.parse_args()

    print 'args', vars(args)

    texts = [line.strip().split('\t', 1)[0].decode('ascii', errors='ignore')
             for line in smart_open(args.bigram_file)]
    run_batched_queries(texts, args.index_path, args.output_file, args.timings_file,
                        k=args.k, threads=args.threads, batch_size=args.batch_size, rule=args.rule)
