import numpy as np
import matplotlib.pyplot as plt
import copy
def calculate_quadrants_sum(input):
    map, index = input
    map = np.array(map)
    middle_x, middle_y = int(len(map[0])/2), int(len(map)/2)
    first_quadrant, second_quadrant = map[:middle_y, middle_x+1:].sum(), map[:middle_y,:middle_x].sum()
    third_quadrant, fourth_quadrant = map[middle_y + 1:, :middle_x].sum(), map[middle_y+1:, middle_x + 1:].sum()
    total = first_quadrant * second_quadrant * third_quadrant * fourth_quadrant
    print(f"The quadrants contain {second_quadrant}, {first_quadrant}, {third_quadrant}, {fourth_quadrant} robots\nSafety factor is: {total}")
    visualise_map(np.array(map), index)

def step(robots, occupancy, max_x, max_y):
    for robot in robots:
        x, y = robot["pos"]
        v_x, v_y = robot["v"]
        new_x, new_y = (x + v_x) % max_x, (y + v_y) % max_y
        occupancy[y][x] -= 1
        robot["pos"] = [new_x, new_y]
        occupancy[new_y][new_x] += 1

    return robots, occupancy

def visualise_map(matrix, index=0):
    rows, cols = np.where(matrix >= 1)
    plt.figure(figsize=(6, 6))
    plt.scatter(cols, rows, color='black', marker='o')
    plt.xlim(-0.5, matrix.shape[1] - 0.5)
    plt.ylim(-0.5, matrix.shape[0] - 0.5)
    plt.gca().invert_yaxis()
    plt.grid(visible=True, which='both', color='gray', linestyle='--', linewidth=0.5)
    plt.title(f"Configuration after {index} seconds")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xticks(ticks=np.arange(matrix.shape[1]))
    plt.yticks(ticks=np.arange(matrix.shape[0]))
    plt.show()

def main(input, seconds=6355):
    robots = []
    x_max, y_max = [int(i) for i in input.splitlines()[-1].split(",")]
    occupancy = [[0 for _ in range(x_max)]for _ in range(y_max)]
    lines = input.splitlines()[:-1]
    for line in lines:
        pos, v = line.split(" ")
        x, y = [int(i) for i in pos.split("=")[1].split(",")]
        occupancy[y][x] += 1
        robot = {"pos": [x, y], "v": [int(i) for i in v.split("=")[1].split(",")]}
        robots.append(robot)
    christmas_tree = None
    for second in range(seconds):
        robots, occupancy = step(robots, occupancy, x_max, y_max)
        if np.all(np.isin(occupancy, [0, 1])):
            christmas_tree = (copy.deepcopy(occupancy), second + 1)
    return christmas_tree if christmas_tree is not None else (occupancy, seconds)

with open("inputs/day14", "r") as file:
    input = file.read()
calculate_quadrants_sum(main(input))