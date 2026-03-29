import argparse, random

def generate(w, h, seed=None):
    if seed: random.seed(seed)
    grid = [[1]*(2*w+1) for _ in range(2*h+1)]
    for y in range(h):
        for x in range(w):
            grid[2*y+1][2*x+1] = 0
    visited = set()
    stack = [(0, 0)]
    visited.add((0, 0))
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            grid[2*y+1+dy][2*x+1+dx] = 0
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
    grid[1][0] = 0  # entrance
    grid[2*h-1][2*w] = 0  # exit
    return grid

def solve(grid):
    h, w = len(grid), len(grid[0])
    start = (0, 1)
    end = (w-1, h-2)
    queue = [start]
    parent = {start: None}
    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            path = set()
            while (x, y) is not None:
                path.add((x, y))
                p = parent.get((x, y))
                if p is None: break
                x, y = p
            return path
        for dx, dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == 0 and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    return set()

def display(grid, path=None):
    for y, row in enumerate(grid):
        line = ""
        for x, cell in enumerate(row):
            if path and (x, y) in path: line += "·"
            elif cell: line += "█"
            else: line += " "
        print(line)

def main():
    p = argparse.ArgumentParser(description="Maze generator/solver")
    p.add_argument("-W", "--width", type=int, default=15)
    p.add_argument("-H", "--height", type=int, default=10)
    p.add_argument("--seed", type=int)
    p.add_argument("--solve", action="store_true")
    args = p.parse_args()
    grid = generate(args.width, args.height, args.seed)
    path = solve(grid) if args.solve else None
    display(grid, path)

if __name__ == "__main__":
    main()
