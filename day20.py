import sys
from heapq import heappush, heappop
def is_in_map(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def manhattan_distance(pos, end):
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def find_shortest_path(pos, is_wall, end): # A*
    priority_queue = []
    visited = set()
    heappush(priority_queue, (manhattan_distance(pos, end), 0, pos))

    while priority_queue:
        total_cost, current_score, pos = heappop(priority_queue)
        i, j = pos
        if not is_in_map(i, j, is_wall) or (i, j) in visited or is_wall[i][j]:
            continue
        visited.add((i, j))
        if (i, j) == end:
            return current_score
        for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            new_i, new_j = i + direction[0], j + direction[1]
            heappush(priority_queue, (
                current_score + 1 + manhattan_distance((new_i, new_j), end),
                current_score + 1,
                (new_i, new_j)
            ))

    return sys.maxsize

def main(input, threashold=100, max_cheat_duration=20, disable_part1=False):
    height, width = len(input.splitlines()), len(input.splitlines()[0])
    is_wall = [[False for _ in range(width)] for _ in range(height)]
    start, end = None, None
    row_cnt = 0
    for line in input.splitlines():
        for j in range(len(line)):
            if line[j] == "S":
                start = (row_cnt, j)
            elif line[j] == "E":
                end = (row_cnt, j)
            elif line[j] == "#":
                is_wall[row_cnt][j] = True
        row_cnt += 1
    shortest_path_length = find_shortest_path(start, is_wall, end)

    if not disable_part1:
        saved_paths = {}
        for i in range(height):
            for j in range(width):
                if is_wall[i][j] and i != 0 and i != height - 1 and j != 0 and j != width - 1:
                    is_wall[i][j] = False
                    saved = shortest_path_length - find_shortest_path(start, is_wall, end)
                    saved_paths[saved] = saved_paths.get(saved, 0) + 1
                    is_wall[i][j] = True
        total = 0
        for second in sorted(saved_paths):
            if second >= threashold:
                total += saved_paths[second]
            print(f"{saved_paths[second]} cheats save {second} picoseconds")
        print(f"\nPart 1: {total} cheats save at least {threashold} seconds")

    # ------------------------ part 2 -----------------------------
    distance_remaining = [[0 for _ in range(width)] for _ in range(height)]
    distance_travelled = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            if not is_wall[i][j]:
                print(f"Calculating travelled and remaining distance for ({i}, {j})")
                distance_travelled[i][j] = find_shortest_path(start, is_wall, (i, j))
                distance_remaining[i][j] = find_shortest_path((i, j), is_wall, end)

    saved_paths = {}
    for i in range(height):
        for j in range(width):
            if not is_wall[i][j]:
                print(f"Checking ({i}, {j})")
                for i_2 in range(height):
                    for j_2 in range(width):
                        if not is_wall[i_2][j_2] and distance_remaining[i_2][j_2] < distance_remaining[i][j] and manhattan_distance((i, j), (i_2, j_2)) <= max_cheat_duration:
                            saved = shortest_path_length - (distance_travelled[i][j] + manhattan_distance((i, j), (i_2, j_2)) + distance_remaining[i_2][j_2])
                            if saved > 0:
                                saved_paths[saved] = saved_paths.get(saved, 0) + 1
    total = 0
    for second in sorted(saved_paths):
        if second >= threashold:
            total += saved_paths[second]
        print(f"{saved_paths[second]} cheats save {second} picoseconds")
    print(f"\nPart 2: {total} cheats save at least {threashold} seconds")

with open("inputs/day20", "r") as file:
    input = file.read()
main(input, disable_part1=True)