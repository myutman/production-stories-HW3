from argparse import ArgumentParser

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

if __name__ == '__main__':
    args = parse_args()

    records = []
    with open(args.input_file) as inf:
        for line in inf.readlines():
            x, y = map(int, line.split(' '))
            records.append((x, y))

    records = sorted(records, key = lambda record: record[0])

    for x, y in records:
        print(x, y)


