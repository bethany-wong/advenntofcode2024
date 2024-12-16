import sys
from heapq import heappush, heappop
from collections import deque

directions = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1)
}

turn = {
    "N": {"CW": "E", "CCW": "W"},
    "E": {"CW": "S", "CCW": "N"},
    "S": {"CW": "W", "CCW": "E"},
    "W": {"CW": "N", "CCW": "S"},
}

def is_in_map(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def visualise_list(is_wall, list):
    print()
    row_cnt = 0
    for line in is_wall:
        row = []
        for j in range(len(line)):
            if (row_cnt, j) in list:
                row.append("O")
            elif line[j]:
                row.append("#")
            else:
                row.append(".")
        row_cnt += 1
        print(row)

def manhattan_distance(pos, end):
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def find_shortest_path(pos, direction, is_wall, end): # A*
    priority_queue = []
    visited = set()
    heappush(priority_queue, (manhattan_distance(pos, end), 0, pos, direction))

    while priority_queue:
        total_cost, current_score, pos, direction = heappop(priority_queue)
        i, j = pos
        if not is_in_map(i, j, is_wall) or (i, j) in visited or is_wall[i][j]:
            continue
        visited.add((i, j))
        if (i, j) == end:
            #visualise_list(is_wall, visited)
            return current_score, direction
        new_pos_straight = (i + directions[direction][0], j + directions[direction][1])
        new_pos_cw = (i + directions[turn[direction]["CW"]][0], j + directions[turn[direction]["CW"]][1])
        new_pos_ccw = (i + directions[turn[direction]["CCW"]][0], j + directions[turn[direction]["CCW"]][1])
        heappush(priority_queue, (
            current_score + 1 + manhattan_distance(new_pos_straight, end),
            current_score + 1,
            new_pos_straight,
            direction
        ))
        heappush(priority_queue, (
            current_score + 1001 + manhattan_distance(new_pos_cw, end),
            current_score + 1001,
            new_pos_cw,
            turn[direction]["CW"]
        ))
        heappush(priority_queue, (
            current_score + 1001 + manhattan_distance(new_pos_ccw, end),
            current_score + 1001,
            new_pos_ccw,
            turn[direction]["CCW"]
        ))

    return sys.maxsize, ""

def find_seats(start, direction, is_wall, end, lowest_score):
    seats = set()
    for i in range(len(is_wall)):
        print("row " + str(i))
        for j in range(len(is_wall[0])):
            if not is_wall[i][j]:
                current_score, current_direction = find_shortest_path(start, direction, is_wall, (i, j))
                if current_score > lowest_score:
                    continue
                score2, _ = find_shortest_path((i, j), current_direction, is_wall, end)
                if current_score + score2 == lowest_score:
                    seats.add((i, j))
    print(len(seats))

def floodfill_recursive(pos, direction, is_wall, end, visited, current_score):
    i, j = pos
    if not is_in_map(i, j, is_wall) or visited[i][j] or is_wall[i][j]:
        return sys.maxsize
    if (i, j) == end:
        return current_score
    visited[i][j] = True
    new_pos_straight = (i + directions[direction][0], j + directions[direction][1])
    new_pos_cw = (i + directions[turn[direction]["CW"]][0], j + directions[turn[direction]["CW"]][1])
    new_pos_ccw = (i + directions[turn[direction]["CCW"]][0], j + directions[turn[direction]["CCW"]][1])
    scores = {"straight": floodfill_recursive(new_pos_straight, direction, is_wall, end, visited, current_score + 1),
              "CW": floodfill_recursive(new_pos_cw, turn[direction]["CW"], is_wall, end, visited, current_score + 1001),
              "CCW": floodfill_recursive(new_pos_ccw, turn[direction]["CCW"], is_wall, end, visited, current_score + 1001)}
    visited[i][j] = False
    return min(scores["CCW"], min(scores["straight"], scores["CW"]))

def main(input):
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
    lowest_score, dir = find_shortest_path(start, "E", is_wall, end)
    print(f"Lowest score: {lowest_score}, facing: {dir}")
    find_seats(start, "E", is_wall, end, lowest_score)

with open("inputs/day16", "r") as file:
    input = file.read()
main(input)