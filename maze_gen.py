#!/usr/bin/env python3
"""Maze Generator - Generate and solve mazes with multiple algorithms."""
import sys, random
from collections import deque

def generate_dfs(rows, cols, seed=None):
    if seed is not None: random.seed(seed)
    maze = [[1]*(2*cols+1) for _ in range(2*rows+1)]
    for r in range(rows):
        for c in range(cols): maze[2*r+1][2*c+1] = 0
    visited = set(); stack = [(0, 0)]; visited.add((0, 0))
    while stack:
        r, c = stack[-1]
        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited:
                neighbors.append((nr, nc, dr, dc))
        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            maze[2*r+1+dr][2*c+1+dc] = 0
            visited.add((nr, nc)); stack.append((nr, nc))
        else: stack.pop()
    return maze

def solve_bfs(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1); end = (rows-2, cols-2)
    queue = deque([(start, [start])]); visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end: return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr,nc) not in visited:
                visited.add((nr,nc)); queue.append(((nr,nc), path + [(nr,nc)]))
    return None

def render(maze, path=None):
    path_set = set(path) if path else set()
    lines = []
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if (r,c) in path_set: line += "·"
            elif cell == 1: line += "█"
            else: line += " "
        lines.append(line)
    return "\n".join(lines)

def main():
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 42
    maze = generate_dfs(rows, cols, seed)
    path = solve_bfs(maze)
    print(f"=== Maze ({rows}x{cols}) ===\n")
    print(render(maze, path))
    print(f"\nPath length: {len(path) if path else 'no solution'}")

if __name__ == "__main__":
    main()
