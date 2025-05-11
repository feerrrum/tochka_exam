import sys

import collections


# Константы для символов ключей и дверей
keys_char = {chr(i) for i in range(ord('a'), ord('z') + 1)}
doors_char = {k.upper() for k in keys_char}


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def get_objects_location(maze: list[list[str]]) -> tuple:
    rows, cols = len(maze), len(maze[0])
    keys = {}
    robots = {}

    for i in range(rows):
        for j in range(cols):
            s = maze[i][j]
            if s in keys_char:
                keys[s] = (i, j)
            if s == '@':
                robots[str(len(robots))] = (i, j)

    return keys, robots


def memoize_bfs(func):
    cache = {}

    def wrapped(maze, start, end, open_doors=None):
        if open_doors is None:
            open_doors = frozenset()
        else:
            open_doors = frozenset(open_doors)
        key = frozenset((start, end, open_doors))
        if key not in cache:
            cache[key] = func(maze, start, end, open_doors)
        return cache[key]

    return wrapped


@memoize_bfs
def bfs(maze: list[list[str]], start: tuple, end: tuple, open_doors=None) -> int:
    if open_doors is None:
        open_doors = set()
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = collections.deque([(start[0], start[1], 0)])
    visited = set()
    visited.add(start)

    while queue:
        x, y, distance = queue.popleft()

        if (x, y) == end:
            return distance

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] not in (doors_char - open_doors | {'#'}):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, distance + 1))

    return -1


def solve(data):
    keys, robots = get_objects_location(data)
    num_of_keys = len(keys)
    d = [[(bfs(data, k_coord, r_coord), key + r) for key, k_coord in keys.items() for r, r_coord in robots.items()]]

    for step in range(1, num_of_keys):
        d.append([])
        for k in keys:
            for r in robots:
                prev_nodes = [node for node in d[step - 1] if node[0] != -1 and k not in node[1]]
                dist_to_prev_nodes = []
                end = keys[k]
                for node in prev_nodes:
                    ind = node[1].rfind(r)
                    if ind != -1:
                        start = keys[node[1][ind - 1]]
                    else:
                        start = robots[r]

                    dist = bfs(data, start, end, {v.upper() for v in node[1][::2]})
                    if dist != -1:
                        dist_to_prev_nodes.append((dist + node[0], node[1] + k + r))

                d[step].append(min(dist_to_prev_nodes, key=lambda x: x[0], default=(-1, '')))

    return min(d[-1], key=lambda x: x[0] if x[0] != -1 else float('inf'), default=(-1, ''))[0]


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
