#!/usr/bin/env python3
import sys


def count_stats(content):
    lines = content.count('\n')
    words = len(content.split())
    bytes_count = len(content.encode('utf-8'))

    return lines, words, bytes_count


def process_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()

        return count_stats(content)
    except FileNotFoundError:
        print(f"wc: {filename}: No such file or directory", file=sys.stderr)
        return None
    except IOError as e:
        print(f"wc: {filename}: {e}", file=sys.stderr)
        return None


def main():
    files = sys.argv[1:]
    
    if not files:
        content = sys.stdin.read()
        lines, words, bytes_count = count_stats(content)
        print(f"{lines:7} {words:7} {bytes_count:7}")
    elif len(files) == 1:
        stats = process_file(files[0])
        if stats:
            lines, words, bytes_count = stats
            print(f"{lines:7} {words:7} {bytes_count:7} {files[0]}")
    else:
        total_lines = 0
        total_words = 0
        total_bytes = 0
        
        for filename in files:
            stats = process_file(filename)
            if stats:
                lines, words, bytes_count = stats
                print(f"{lines:7} {words:7} {bytes_count:7} {filename}")
                total_lines += lines
                total_words += words
                total_bytes += bytes_count
        
        print(f"{total_lines:7} {total_words:7} {total_bytes:7} total")


if __name__ == "__main__":
    main()
