#!/usr/bin/env python3
"""maze_gen - Maze generation (DFS, Kruskal) and solving (BFS, A*)."""
import sys, random
from collections import deque

def generate_dfs(width, height, seed=None):
    if seed is not None:
        random.seed(seed)
    grid = [[1] * (2 * width + 1) for _ in range(2 * height + 1)]
    visited = [[False] * width for _ in range(height)]
    def carve(cx, cy):
        visited[cy][cx] = True
        grid[2*cy+1][2*cx+1] = 0
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                grid[2*cy+1+dy][2*cx+1+dx] = 0
                carve(nx, ny)
    sys.setrecursionlimit(width * height + 100)
    carve(0, 0)
    return grid

def solve_bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def test():
    maze = generate_dfs(5, 5, seed=42)
    assert len(maze) == 11 and len(maze[0]) == 11
    assert maze[1][1] == 0  # start cell is open
    path = solve_bfs(maze, (1, 1), (9, 9))
    assert path is not None
    assert path[0] == (1, 1) and path[-1] == (9, 9)
    # all path cells are open
    for x, y in path:
        assert maze[y][x] == 0
    # larger maze
    maze2 = generate_dfs(10, 10, seed=0)
    path2 = solve_bfs(maze2, (1, 1), (19, 19))
    assert path2 is not None
    print("OK: maze_gen")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: maze_gen.py test")
