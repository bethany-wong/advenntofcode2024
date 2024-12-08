import numpy as np

def is_in_map(pos, r, c):
    return pos[0] >= 0 and pos[0] < r and pos[1] >= 0 and pos[1] < c

def main(input):
    map = {}
    row_cnt = 0
    for line in input.splitlines():
        for col in range(len(line)):
            antenna = line[col]
            if antenna != ".":
                if antenna not in map:
                    map[antenna] = []
                map[antenna].append([row_cnt, col])
        row_cnt += 1
    row_max = row_cnt
    col_max = len(input.splitlines()[0])

    antinodes  = [[False for _ in range(col_max)] for _ in range(row_max)]
    antinodes_part2 = [[False for _ in range(col_max)] for _ in range(row_max)]
    for antenna_name in map:
        antenna_lst = map[antenna_name]
        for i in range(len(antenna_lst)):
            for j in range(len(antenna_lst)):
                if i != j:
                    i_row, i_col = antenna_lst[i]
                    j_row, j_col = antenna_lst[j]
                    vector = [i_row - j_row, i_col - j_col]
                    potential_antinode = [i_row + vector[0], i_col + vector[1]] # a + ba
                    if is_in_map(potential_antinode, row_max, col_max):
                        antinodes[potential_antinode[0]][potential_antinode[1]] = True
                    # -------------------------- part 2 ---------------------------
                    distance = 1
                    potential_antinode = [j_row + vector[0], j_col + vector[1]] # b +  distance * bas
                    while is_in_map(potential_antinode, row_max, col_max):
                        antinodes_part2[potential_antinode[0]][potential_antinode[1]] = True
                        distance += 1
                        potential_antinode = [j_row + distance * vector[0], j_col + distance * vector[1]]
                    # -------------------------------------------------------------

    print(f"Number of distinct antinodes is: {np.array(antinodes).sum()}\nNumber of distinct antinodes for part 2 is: {np.array(antinodes_part2).sum()}")

with open("inputs/day8", "r") as file:
    input = file.read()
main(input)