import argparse
import sh


def get_estimates(iterable):
    for line in iterable:
        epsilon, prune_ratio = map(float, line.split())
        yield epsilon, round(prune_ratio, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('estimate_file')
    parser.add_argument('ratio', type=float)
    args = parser.parse_args()

    est = {r: e for e, r in get_estimates(file(args.estimate_file))}
    print est[args.ratio]
