import argparse

import lenses  # type: ignore


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to recursively search for photos")
    return parser.parse_args()


def main():
    args = parse_args()
    lenses.main(args.path)


if __name__ == '__main__':
    main()
