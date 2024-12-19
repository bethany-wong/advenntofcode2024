from heapq import heappush, heappop
import sys

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

def main(input, map_size=7, num_falling_bytes=12):
    falling_bytes = [tuple(line.split(',')) for line in input.splitlines()]
    print(falling_bytes)
    map = [[False for _ in range(map_size)] for _ in range(map_size)]
    for byte in range(num_falling_bytes):
        i, j = int(falling_bytes[byte][0]), int(falling_bytes[byte][1])
        map[i][j] = True
    print(find_shortest_path((0, 0), map, (map_size - 1, map_size - 1)))

    for byte in range(num_falling_bytes, len(falling_bytes)):
        print(byte)
        i, j = int(falling_bytes[byte][0]), int(falling_bytes[byte][1])
        map[i][j] = True
        if find_shortest_path((0, 0), map, (map_size - 1, map_size - 1)) == sys.maxsize:
            print(f"{i},{j}")
            break

with open("inputs/day18", "r") as file:
    input = file.read()
main(input, map_size=71, num_falling_bytes=1024)