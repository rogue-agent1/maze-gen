#!/usr/bin/env python3
"""Random maze generator (recursive backtracker)."""
import sys, random

def generate(w, h, seed=None):
    if seed is not None: random.seed(seed)
    grid = [[0]*w for _ in range(h)]
    visited = [[False]*w for _ in range(h)]
    dirs = [(0,-1,1),(0,1,4),(1,0,8),(-1,0,2)]  # dx,dy,wall

    def carve(x, y):
        visited[y][x] = True
        ds = list(dirs)
        random.shuffle(ds)
        for dx, dy, wall in ds:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                grid[y][x] |= wall
                opp = {1:4,4:1,2:8,8:2}
                grid[ny][nx] |= opp[wall]
                carve(nx, ny)

    carve(0, 0)
    return grid

def render(grid):
    h, w = len(grid), len(grid[0])
    lines = []
    lines.append('┌' + '┬'.join('───' for _ in range(w)) + '┐')
    for y in range(h):
        row = '│'
        for x in range(w):
            row += '   '
            row += ' ' if grid[y][x] & 8 else '│'
        lines.append(row)
        if y < h-1:
            sep = '├'
            for x in range(w):
                sep += '   ' if grid[y][x] & 4 else '───'
                sep += '┼' if x < w-1 else '┤'
            lines.append(sep)
    lines.append('└' + '┴'.join('───' for _ in range(w)) + '┘')
    return '\n'.join(lines)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-W', '--width', type=int, default=10)
    p.add_argument('-H', '--height', type=int, default=10)
    p.add_argument('-s', '--seed', type=int)
    args = p.parse_args()
    print(render(generate(args.width, args.height, args.seed)))
