#!/usr/bin/env python3
"""maze_gen - Random maze generator and solver."""
import sys, argparse, json, random
from collections import deque

def generate(w, h, seed=None):
    if seed: random.seed(seed)
    maze = [[1]*(2*w+1) for _ in range(2*h+1)]
    for y in range(h):
        for x in range(w):
            maze[2*y+1][2*x+1] = 0
    visited = set(); stack = [(0,0)]
    visited.add((0,0))
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in visited:
                neighbors.append((nx,ny,dx,dy))
        if neighbors:
            nx,ny,dx,dy = random.choice(neighbors)
            maze[2*y+1+dy][2*x+1+dx] = 0
            visited.add((nx,ny))
            stack.append((nx,ny))
        else:
            stack.pop()
    maze[1][0] = 0; maze[2*h-1][2*w] = 0
    return maze

def solve(maze):
    h, w = len(maze), len(maze[0])
    start = (0, 1); end = (w-1, h-2)
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (x,y), path = queue.popleft()
        if (x,y) == end: return path
        for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and maze[ny][nx]==0 and (nx,ny) not in visited:
                visited.add((nx,ny))
                queue.append(((nx,ny), path+[(nx,ny)]))
    return []

def render(maze, path=None):
    path_set = set(path) if path else set()
    lines = []
    for y, row in enumerate(maze):
        line = ""
        for x, cell in enumerate(row):
            if (x,y) in path_set: line += "·"
            elif cell == 1: line += "█"
            else: line += " "
        lines.append(line)
    return "
".join(lines)

def main():
    p = argparse.ArgumentParser(description="Maze generator")
    p.add_argument("width", type=int, nargs="?", default=10)
    p.add_argument("height", type=int, nargs="?", default=10)
    p.add_argument("--seed", type=int)
    p.add_argument("--solve", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    maze = generate(args.width, args.height, args.seed)
    path = solve(maze) if args.solve else None
    if args.json:
        print(json.dumps({"width": args.width, "height": args.height, "path_length": len(path) if path else 0}))
    else:
        print(render(maze, path))

if __name__ == "__main__": main()
