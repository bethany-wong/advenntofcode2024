import numpy as np
def main(input, height=5):
    input = input.split("\n\n")
    keys, locks = [], []
    for grid in input:
        rows = np.array([list(line) for line in grid.splitlines()])
        pin_heights = []
        for i in range(len(rows[0])):
            pin_heights.append(np.sum(rows[1:-1, i] == "#"))
        if rows[0][0] == "#": # locks
            locks.append(pin_heights)
        else: # keys
            keys.append(pin_heights)

    total = 0
    for key in keys:
        for lock in locks:
            if np.all([key[i] + lock[i] <= height for i in range(len(key))]):
                total += 1
    print(f"Number of unique lock/key pairs: {total}")

with open("inputs/day25", "r") as file:
    input = file.read()
main(input)