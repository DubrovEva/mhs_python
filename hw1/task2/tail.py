#!/usr/bin/env python3

import sys
from collections import deque

def tail_file(file, num_lines=10):
    return deque(file, maxlen=num_lines)


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        multiple_files = len(files) > 1
        
        for i, filename in enumerate(files):
            if multiple_files:
                if i > 0:
                    print()
                print(f"==> {filename} <==")
            
            try:
                with open(filename, 'r') as f:
                    lines = tail_file(f, num_lines=10)
                    for line in lines:
                        print(line, end='')
            except FileNotFoundError:
                print(f"tail.py: cannot open '{filename}' for reading: No such file or directory", file=sys.stderr)
                sys.exit(1)
            except IOError as e:
                print(f"tail.py: {filename}: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        lines = tail_file(sys.stdin, num_lines=17)
        for line in lines:
            print(line, end='')


if __name__ == "__main__":
    main()
