#!/usr/bin/env python3
"""Maze generator and solver — DFS generation, BFS/DFS solving."""
import sys, random
from collections import deque

class Maze:
    def __init__(self, w=21, h=11):
        self.w = w | 1; self.h = h | 1  # ensure odd
        self.grid = [['#'] * self.w for _ in range(self.h)]
    def generate(self, seed=None):
        if seed is not None: random.seed(seed)
        stack = [(1, 1)]
        self.grid[1][1] = ' '
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(0,2),(0,-2),(2,0),(-2,0)]:
                nx, ny = x+dx, y+dy
                if 0 < nx < self.w-1 and 0 < ny < self.h-1 and self.grid[ny][nx] == '#':
                    neighbors.append((nx, ny, x+dx//2, y+dy//2))
            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                self.grid[wy][wx] = ' '
                self.grid[ny][nx] = ' '
                stack.append((nx, ny))
            else:
                stack.pop()
        self.start = (1, 1); self.end = (self.w-2, self.h-2)
    def solve_bfs(self):
        q = deque([(self.start, [self.start])])
        visited = {self.start}
        while q:
            (x, y), path = q.popleft()
            if (x, y) == self.end: return path
            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.w and 0 <= ny < self.h and self.grid[ny][nx] == ' ' and (nx,ny) not in visited:
                    visited.add((nx, ny))
                    q.append(((nx, ny), path + [(nx, ny)]))
        return []
    def render(self, path=None):
        path_set = set(path) if path else set()
        lines = []
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if (x, y) == self.start: row += "S"
                elif (x, y) == self.end: row += "E"
                elif (x, y) in path_set: row += "·"
                elif self.grid[y][x] == '#': row += "█"
                else: row += " "
            lines.append(row)
        return "\n".join(lines)

if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    m = Maze(w, h)
    m.generate(42)
    path = m.solve_bfs()
    print(m.render(path))
    print(f"\nMaze: {m.w}x{m.h}, Path length: {len(path)}")
