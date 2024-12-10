import numpy as np
def is_in_map(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def find_score(current_pos, map, visited, ends):
    i, j = current_pos
    if not is_in_map(i, j, map):
        return ends
    if visited[i][j]:
        return ends
    if map[i][j] == 9:
        ends.add((i, j))
        return ends
    visited[i][j] = True
    for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        new_i, new_j = i + direction[0], j+direction[1]
        if is_in_map(new_i, new_j, map) and map[new_i][new_j] == map[i][j] + 1:
            ends |= find_score([new_i, new_j], map, visited, ends)
    return ends

def find_score_part2(current_pos, map, visited, ends, code):
    i, j = current_pos
    if not is_in_map(i, j, map):
        return ends
    if visited[i][j]:
        return ends
    code = f'{code}{i}{j}'
    if map[i][j] == 9:
        ends.add(code)
        return ends
    visited[i][j] = True
    for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        new_i, new_j = i + direction[0], j+direction[1]
        if is_in_map(new_i, new_j, map) and map[new_i][new_j] == map[i][j] + 1:
            ends |= find_score_part2([new_i, new_j], map, visited, ends, code)
    visited[i][j] = False
    return ends

def main(input):
    trailheads, map = [], []
    row_cnt = 0
    for line in input.splitlines():
        row = []
        for col in range(len(line)):
            if line[col] == "0":
                trailheads.append((row_cnt, col))
            row.append(int(line[col]))
        map.append(row)
        row_cnt += 1
    col_cnt = len(map[0])
    total_score, total_part2 = 0, 0
    for trailhead in trailheads:
        total_score += len(find_score(trailhead, map, [[False for _ in range(col_cnt)] for _ in range(row_cnt)], set()))
        total_part2 += len(find_score_part2(trailhead, map, [[False for _ in range(col_cnt)] for _ in range(row_cnt)], set(), ""))
    print(f'Part 1: {total_score}\nPart 2: {total_part2}')

with open("inputs/day10", "r") as file:
    input = file.read()
main(input)