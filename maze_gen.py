#!/usr/bin/env python3
"""maze_gen - Generate and solve random mazes using DFS."""
import sys, random
def generate(w, h, seed=None):
    if seed: random.seed(seed)
    maze = [[1]*(2*w+1) for _ in range(2*h+1)]
    for r in range(h):
        for c in range(w): maze[2*r+1][2*c+1] = 0
    visited = set(); stack = [(0, 0)]; visited.add((0, 0))
    while stack:
        r, c = stack[-1]
        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in visited:
                neighbors.append((nr, nc, dr, dc))
        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            maze[2*r+1+dr][2*c+1+dc] = 0
            visited.add((nr, nc)); stack.append((nr, nc))
        else: stack.pop()
    maze[1][0] = 0; maze[2*h-1][2*w] = 0
    return maze
def solve(maze):
    h, w = len(maze), len(maze[0])
    start = (1, 0); end = (h-2, w-1)
    visited = set(); stack = [start]; parent = {}
    while stack:
        r, c = stack.pop()
        if (r, c) == end:
            path = set()
            while (r, c) in parent: path.add((r, c)); r, c = parent[(r, c)]
            path.add(start); return path
        if (r, c) in visited: continue
        visited.add((r, c))
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and maze[nr][nc] == 0 and (nr, nc) not in visited:
                parent[(nr, nc)] = (r, c); stack.append((nr, nc))
    return set()
def display(maze, path=None):
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if path and (r, c) in path: line += "·"
            elif cell == 1: line += "█"
            else: line += " "
        print(line)
if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else None
    maze = generate(w, h, seed)
    show_solution = "--solve" in sys.argv
    path = solve(maze) if show_solution else None
    display(maze, path)
