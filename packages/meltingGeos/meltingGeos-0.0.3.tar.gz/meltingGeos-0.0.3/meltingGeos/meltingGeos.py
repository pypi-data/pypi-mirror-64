#! /usr/bin/env python3

from argparse import ArgumentParser
from libgs import Geos

def findArgSeach():
    parser = ArgumentParser(description="Process parser")
    parser.add_argument('--search', help='search city name')
    parser.add_argument('--depth', type=int, help='search depth')
    
    # Pars arg search; if --search abc; return abc;
    if parser.parse_args().search == None:
        exit(f"error: meltingGeos need argument --search")
    if parser.parse_args().depth == None:
        exit(f"error: meltingGeos need argument --depth")
    return parser.parse_args()


if __name__ == "__main__":
    args = findArgSeach()
    print(Geos().findall(args.search, args.depth))


