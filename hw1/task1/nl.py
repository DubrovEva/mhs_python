#!/usr/bin/env python3

import sys

def number_lines(file):
    for number, line in enumerate(file, 1):
        line = line.rstrip('\n')

        print(f"{number:6}\t{line}")


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        try:
            with open(filename, 'r') as f:
                number_lines(f)
        except FileNotFoundError:
            print(f"nl.py: {filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"nl.py: {filename}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        number_lines(sys.stdin)


if __name__ == "__main__":
    main()
