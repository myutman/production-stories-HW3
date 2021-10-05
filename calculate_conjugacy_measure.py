from argparse import ArgumentParser

import numpy as np


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--input-file',
        required=True
    )
    parser.add_argument(
        '--output-file',
        required=True
    )
    return parser.parse_args()


def read_data(input_file):
    records = []
    with open(input_file) as inf:
        for line in inf.readlines():
            x, y = map(int, line.split(' '))
            records.append((x, y))
    return records


def sort_records_by_x(records):
    return sorted(records, key = lambda record: record[0])


def get_y_ranks(records):
    ranks = [0 for _ in records]
    ys_with_order = [(y, order) for order, (_, y) in enumerate(records)]
    ys_with_order_sorted = sorted(ys_with_order, key = lambda y_with_order: y_with_order[0])
    for rank, (_, order) in enumerate(ys_with_order_sorted):
        ranks[order] = rank
    return ranks


def calculate_r1_r2(ranks):
    p = len(ranks) // 3
    r1 = sum(ranks[:p])
    r2 = sum(ranks[-p:])
    return r1, r2

if __name__ == '__main__':
    args = parse_args()

    records = read_data(args.input_file)
    records = sort_records_by_x(records)
    ranks = get_y_ranks(records)

    for rank, (x, y) in zip(ranks, records):
        print(x, y, rank)

    r1, r2 = calculate_r1_r2(ranks)
    print(r1, r2)

    N = len(records)
    p = N // 3
    rank_diff = r1 - r2
    std_dev = int((N + 0.5) * np.sqrt(p / 6))
    conjugacy_measure = rank_diff / (p * (N - p))

    print(rank_diff, std_dev, conjugacy_measure)

    with open(args.output_file, "w") as ouf:
        ouf.write(f"{rank_diff} {std_dev} {conjugacy_measure}\n")
