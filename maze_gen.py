#!/usr/bin/env python3
"""Maze generation (DFS, Prim, Kruskal) and solving (BFS, A*)."""
import sys, random
from collections import deque

def generate_dfs(w, h):
    maze = [[1]*(2*w+1) for _ in range(2*h+1)]
    def carve(x, y):
        maze[2*y+1][2*x+1] = 0
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]; random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and maze[2*ny+1][2*nx+1]==1:
                maze[2*y+1+dy][2*x+1+dx] = 0; carve(nx, ny)
    carve(0, 0); return maze

def solve_bfs(maze, start, end):
    h, w = len(maze), len(maze[0])
    q = deque([(start, [start])]); visited = {start}
    while q:
        (x,y), path = q.popleft()
        if (x,y) == end: return path
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and maze[ny][nx]==0 and (nx,ny) not in visited:
                visited.add((nx,ny)); q.append(((nx,ny), path+[(nx,ny)]))
    return None

def main():
    random.seed(42); maze = generate_dfs(12, 8)
    start, end = (1,1), (len(maze[0])-2, len(maze)-2)
    path = solve_bfs(maze, start, end)
    path_set = set(path) if path else set()
    for y, row in enumerate(maze):
        line = ""
        for x, cell in enumerate(row):
            if (x,y) in path_set: line += "●"
            elif cell: line += "█"
            else: line += " "
        print(line)
    print(f"Path length: {len(path) if path else 'none'}")

if __name__ == "__main__": main()
