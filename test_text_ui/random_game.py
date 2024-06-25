#!/usr/bin/env python3
import argparse
import random


def all_moves(width: int, height: int):
    return [ 
            f"h {r} {c}" 
            for r in range(height+1) for c in range(width)
    ] + [
            f"v {r} {c}" 
            for r in range(height) for c in range(width+1)
    ]


parser = argparse.ArgumentParser()
parser.add_argument("height", type=int, help="Height of the game board")
parser.add_argument("width", type=int, help="Width of the game board")
parser.add_argument("name", type=str, help="Name of the test case")
args = parser.parse_args()

filename = f"{args.name}_{args.width}x{args.height}.txt"

with open(filename, "w") as f:
    moves = all_moves(args.width, args.height)
    random.shuffle(moves)
    moves += moves[:random.randint(1, len(moves)//2)]
    random.shuffle(moves)
    
    f.write(f"{args.width}\n{args.height}\n")
    f.write("\n".join(moves))
    f.write("\n")
    
    