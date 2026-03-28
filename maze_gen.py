#!/usr/bin/env python3
"""maze_gen - Generate and solve mazes."""
import argparse, random, sys
from collections import deque

def generate(w, h, seed=None):
    if seed is not None: random.seed(seed)
    grid = [[0]*w for _ in range(h)]
    visited = [[False]*w for _ in range(h)]
    dirs = [(0,-1,1),(0,1,4),(1,0,8),(-1,0,2)]  # dx,dy,wall
    opp = {1:4,4:1,8:2,2:8}
    def dfs(x, y):
        visited[y][x] = True
        random.shuffle(dirs)
        for dx, dy, wall in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and not visited[ny][nx]:
                grid[y][x] |= wall
                grid[ny][nx] |= opp[wall]
                dfs(nx, ny)
    dfs(0, 0)
    return grid

def render(grid, w, h, path=None):
    path_set = set(path) if path else set()
    lines = []
    for y in range(h):
        top = ""; mid = ""
        for x in range(w):
            top += "+" + ("   " if grid[y][x] & 1 else "---")
            ch = " * " if (x,y) in path_set else "   "
            mid += ((" " if grid[y][x] & 2 else "|") + ch)
        top += "+"; mid += "|"
        lines.extend([top, mid])
    lines.append("+" + "---+" * w)
    return "\n".join(lines)

def solve(grid, w, h):
    q = deque([(0,0,[(0,0)])])
    visited = {(0,0)}
    dirs = [(0,-1,1),(0,1,4),(1,0,8),(-1,0,2)]
    while q:
        x, y, path = q.popleft()
        if x == w-1 and y == h-1: return path
        for dx, dy, wall in dirs:
            if grid[y][x] & wall:
                nx, ny = x+dx, y+dy
                if (nx,ny) not in visited:
                    visited.add((nx,ny))
                    q.append((nx,ny,path+[(nx,ny)]))
    return []

def main():
    p = argparse.ArgumentParser(description="Maze generator & solver")
    p.add_argument("-W","--width",type=int,default=15)
    p.add_argument("-H","--height",type=int,default=10)
    p.add_argument("-s","--seed",type=int)
    p.add_argument("--solve",action="store_true")
    a = p.parse_args()
    grid = generate(a.width, a.height, a.seed)
    path = solve(grid, a.width, a.height) if a.solve else None
    print(render(grid, a.width, a.height, path))

if __name__ == "__main__": main()
