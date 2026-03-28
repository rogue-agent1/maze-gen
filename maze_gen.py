#!/usr/bin/env python3
"""maze_gen - Generate random mazes using recursive backtracking."""
import sys, random

def generate(w, h):
    grid = [[0]*w for _ in range(h)]
    visited = [[False]*w for _ in range(h)]
    dirs = [(0,-1,1),(0,1,4),(1,0,8),(-1,0,2)]  # dx,dy,wall
    def carve(x, y):
        visited[y][x] = True
        random.shuffle(dirs)
        for dx, dy, wall in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and not visited[ny][nx]:
                grid[y][x] |= wall
                grid[ny][nx] |= {1:4,4:1,8:2,2:8}[wall]
                carve(nx, ny)
    carve(0, 0)
    return grid

def render(grid):
    h, w = len(grid), len(grid[0])
    lines = []
    lines.append('┌' + '┬'.join('───' for _ in range(w)) + '┐')
    for y in range(h):
        row = '│'
        bottom = '├' if y < h-1 else '└'
        for x in range(w):
            row += '   '
            row += ' ' if grid[y][x] & 8 else '│'
            if y < h-1:
                bottom += '   ' if grid[y][x] & 4 else '───'
                bottom += '┼' if x < w-1 else ('┤' if y < h-1 else '┘')
            else:
                bottom += '───'
                bottom += '┴' if x < w-1 else '┘'
        lines.append(row)
        lines.append(bottom)
    return '\n'.join(lines)

def main():
    args = sys.argv[1:]
    w = int(args[0]) if args and args[0].isdigit() else 10
    h = int(args[1]) if len(args)>1 and args[1].isdigit() else w
    if '-h' in args and not args[0].isdigit():
        print("Usage: maze_gen.py [WIDTH] [HEIGHT] [--seed N]"); return
    if '--seed' in args: random.seed(int(args[args.index('--seed')+1]))
    print(render(generate(w, h)))

if __name__ == '__main__': main()
