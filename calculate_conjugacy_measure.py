import sys

from argparse import ArgumentParser

import numpy as np
import pandas as pd


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


def verify_column(column):
    return (column.dtype == np.float64 or column.dtype == np.int64) and (not np.isnan(column).any())


def read_data(input_file):
    records = pd.read_csv(input_file, delimiter=" ", names=["x", "y"])
    if (not verify_column(records["x"])) or (not verify_column(records["y"])):
        sys.stderr.write(f"Probably input format is incorrect.\nPlease make sure that input file contains sequence of rows containing space-separated pairs of integers.\n\n")
        exit(0)

    if len(records) < 9:
        sys.stderr.write(f"Statistical test is only applicable to a sequence with at least 9 elements.\nInput file contains only {len(records)} lines which is less than needed.\n\n")
        exit(0)

    return records


def sort_records_by_x(records):
    return records.sort_values(by=["x"], ignore_index=True)


def get_y_ranks(records):
    N = len(records)
    records["rank"] = 0

    sorting_order = records.sort_values(by=["y"]).index
    records["rank"][sorting_order] = np.arange(N)[::-1]

    subdfs = []
    for _, subdf in records.groupby(by=["y"]):
        subdf["rank"] = subdf["rank"].mean()
        subdfs.append(subdf)

    records = pd.concat(subdfs).sort_index()

    return records["rank"]


def calculate_stats(ranks):
    N = len(ranks)
    p = N // 3
    r1 = ranks[:p].sum()
    r2 = ranks[-p:].sum()
    rank_diff = round(r1 - r2)
    std_dev = round((N + 0.5) * np.sqrt(p / 6))
    conjugacy_measure = rank_diff / (p * (N - p))
    return rank_diff, std_dev, conjugacy_measure


if __name__ == '__main__':
    args = parse_args()

    records = read_data(args.input_file)

    records = sort_records_by_x(records)
    ranks = get_y_ranks(records)

    rank_diff, std_dev, conjugacy_measure = calculate_stats(ranks)

    with open(args.output_file, "w") as ouf:
        ouf.write(f"{rank_diff} {std_dev} {conjugacy_measure:.2}\n")
