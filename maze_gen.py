#!/usr/bin/env python3
"""Maze generator and solver — DFS generation, BFS/A* solving."""
import sys, random
from collections import deque

def generate(rows, cols, seed=None):
    if seed is not None: random.seed(seed)
    maze = [[1]*(2*cols+1) for _ in range(2*rows+1)]
    visited = [[False]*cols for _ in range(rows)]
    def dfs(r, c):
        visited[r][c] = True
        maze[2*r+1][2*c+1] = 0
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                maze[2*r+1+dr][2*c+1+dc] = 0
                dfs(nr, nc)
    dfs(0, 0)
    return maze

def solve_bfs(maze):
    rows, cols = len(maze), len(maze[0])
    start, end = (1, 1), (rows-2, cols-2)
    q = deque([(start, [start])])
    visited = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end: return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return None

def to_string(maze, path=None):
    path_set = set(path) if path else set()
    lines = []
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) in path_set: line += "."
            elif cell == 1: line += "#"
            else: line += " "
        lines.append(line)
    return chr(10).join(lines)

def test():
    m = generate(5, 5, seed=42)
    assert len(m) == 11 and len(m[0]) == 11
    assert m[1][1] == 0  # start cell open
    path = solve_bfs(m)
    assert path is not None
    assert path[0] == (1, 1) and path[-1] == (9, 9)
    s = to_string(m, path)
    assert "#" in s and "." in s
    print("  maze_gen: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else:
        m = generate(10, 10)
        path = solve_bfs(m)
        print(to_string(m, path))
