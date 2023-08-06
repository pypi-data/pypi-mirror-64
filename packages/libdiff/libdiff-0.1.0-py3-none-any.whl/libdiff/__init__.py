"""
    libdiff
    ~~~~~~~

    libdiff is check diff with line by line
"""
import argparse

from libdiff.bin import diff_bin

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, help='base file')
    parser.add_argument('--target', required=True, help='target file')
    args = parser.parse_args()
    diff_bin(args.base, args.target)

__version__ = '0.1.0'
