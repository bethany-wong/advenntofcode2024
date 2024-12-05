import numpy as np
def count_occurence(str, substr, return_indices=False):
    count = 0
    middle_indices = []
    for pointer in range(len(str) - len(substr) + 1):
        if substr == str[pointer:pointer + len(substr)]:
            count += 1
            middle_indices.append(pointer + int(len(substr)/2))

    return middle_indices if return_indices else count

def count_substr(str, substr, return_indices=False):
    return count_occurence(str, substr, return_indices) + count_occurence(str, substr[::-1], return_indices)

def main(input):
    total = 0

    lines = input.splitlines()
    row_length = len(lines)
    for line in lines:
        total += count_substr(line, "XMAS")

    column_length = len(lines[0])
    for col in range(column_length):
        total += count_substr("".join([lines[i][col] for i in range(row_length)]), "XMAS")

    map = np.array([[0 for _ in range(column_length)] for _ in range(row_length)])
    diagonal_start_indices_lr = [[i, 0] for i in range(1, row_length)] + [[0,j] for j in range(column_length)]
    diagonal_start_indices_rl = [[i, 0] for i in range(row_length)] + [[row_length - 1, j] for j in
                                                                       range(1, column_length)]
    for i_increase in [1, -1]: # combine two diagonal cases together
        start_indices = diagonal_start_indices_lr if i_increase > 0 else diagonal_start_indices_rl
        for start in start_indices:
            diag_str_lst = []
            i, j = start[0], start[1]
            while i >= 0 and i < row_length and j < column_length:
                diag_str_lst.append(lines[i][j])
                i += i_increase
                j += 1
            total += count_substr("".join(diag_str_lst), "XMAS")
            # ------------------------------ part 2 ---------------------------------
            middle_indices = count_substr("".join(diag_str_lst), "MAS", return_indices=True)
            i, j = start[0], start[1]
            pointer = 0
            while i < row_length and j < column_length:
                if pointer in middle_indices:
                    map[i][j] += 1
                i += i_increase
                j += 1
                pointer += 1
            # ------------------------------------------------------------------------

    print(f"Number of XMAS is : {total}\nNumber of X-MAS is: {np.sum(map == 2)}")

with open('inputs/day4', 'r') as file:
    input = file.read()
main(input)
