import numpy as np

directions = {"^": [-1,0], ">": [0, 1], "v": [1, 0], "<": [0, -1]}
turn_right = {"^": ">", ">": "v", "v": "<", "<": "^"}

def is_in_map(pos, r, c):
    return pos[0] >= 0 and pos[0] < r and pos[1] >= 0 and pos[1] < c

def main(input, solve_part_2=True):
    map = []
    guard = None

    row_cnt = 0
    for line in input.splitlines():
        row = []
        for c in range(len(line)):
            if line[c] in directions:
                guard = [row_cnt, c, line[c]]
                row.append(".")
            else:
                row.append(line[c])
        map.append(row)
        row_cnt += 1

    guard_init = [guard[i] for i in range(len(guard))]
    row_num = len(map)
    col_num = len(map[0])
    visited = [[False for _ in range(col_num)] for _ in range(row_num)]

    while is_in_map(guard, row_num, col_num):
        visited[guard[0]][guard[1]] = True
        guard = step(map, guard, row_num, col_num)
        if guard is None:
            break

    print(np.array(visited).sum())

    # -------------------------- part 2 ------------------------------

    if solve_part_2:
        obstruction_possibilities = [[False for _ in range(col_num)] for _ in range(row_num)]
        visited_row, visited_col = np.where(visited)
        for pos in list(zip(visited_row, visited_col)):
            map[pos[0]][pos[1]] = "#"
            if find_loop(map, guard_init, row_num, col_num):
                obstruction_possibilities[pos[0]][pos[1]] = True
            map[pos[0]][pos[1]] = "."

        obstruction_possibilities[guard_init[0]][guard_init[1]] = False
        print(np.array(obstruction_possibilities).sum())

def find_loop(map, guard, row_num, col_num): # hare algorithm
    x, y, dir = guard
    guards = [[x, y, dir], [x, y, dir]] # slow and fast guard
    while is_in_map([guards[0][0], guards[0][1]], row_num, col_num) and is_in_map([guards[1][0], guards[1][1]], row_num, col_num):
        for i in range(2):
            guards[i] = step(map, guards[i], row_num, col_num)
            if guards[i] is None:
                return False
            if i == 1:
                guards[i] = step(map, guards[i], row_num, col_num)
                if guards[i] is None:
                    return False
        if guards[0] == guards[1]:
            return True
    return False

def step(map, guard, row_num, col_num):
    x, y, dir = guard
    next_x = x + directions[dir][0]
    next_y = y + directions[dir][1]
    if is_in_map([next_x, next_y], row_num, col_num):
        if map[next_x][next_y] == '#':
            return [x, y, turn_right[dir]]
        else:
            return [next_x, next_y, dir]
    return None

with open('inputs/day6', 'r') as file:
    input = file.read()
main(input)