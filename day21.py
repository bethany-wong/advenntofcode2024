from heapq import heappush, heappop
import numpy as np
import random
from functools import lru_cache

button2coordinate = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}

def manhattan_distance(pos, end):
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def is_in_map(x, y, width, height, forbidden_area):
    return x >= 0 and x < width and y >= 0 and y < height and (x, y) not in forbidden_area

def perpendicular_deviation(gradient, target):
    target_norm = np.linalg.norm(target)
    if target_norm == 0:
        return np.linalg.norm(gradient)
    projection = np.dot(gradient, target) / target_norm
    perpendicular = gradient - projection * np.array(target) / target_norm
    return np.linalg.norm(perpendicular)

def find_shortest_path(pos, end, width, height, forbidden_area, hyperparameters, is_numberpad=False): # A*
    priority_queue = []
    visited = set()
    heappush(priority_queue, (manhattan_distance(pos, end), "", pos, (0, 0)))

    direction_dict = {
        (1, 0): ">",
        (-1, 0): "<",
        (0, 1): "v",
        (0, -1): "^"
    }

    while priority_queue:
        total_cost, sequence, pos, gradient = heappop(priority_queue)
        x, y = pos
        if not is_in_map(x, y, width, height, forbidden_area) or (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == end:
            return sequence

        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + direction[0], y + direction[1]
            direction_symbol = direction_dict[direction]

            new_gradient = (gradient[0] + direction[0], gradient[1] + direction[1])
            target_direction = (end[0] - x, end[1] - y)
            deviation_penalty = perpendicular_deviation(new_gradient, target_direction) * hyperparameters[2]

            next_total_cost = manhattan_distance(pos, button2coordinate[direction_symbol]) + manhattan_distance((new_x, new_y), end) + deviation_penalty
            if len(sequence) >= 1 and direction_symbol != sequence[-1]: # penalty for not pressing the same button as last time
                next_total_cost += hyperparameters[0]
            if direction[0] != 0:
                next_total_cost += hyperparameters[1]/2
            if not is_numberpad and x == 1 and new_x != 1: # penalty for moving away from center of the panel
                next_total_cost += hyperparameters[1]
            heappush(priority_queue, (
                next_total_cost,
                sequence + direction_symbol,
                (new_x, new_y),
                new_gradient
            ))

    return ""

def find_sequence_number_pad(code, hyperpameters):
    number2coordinate = [(1, 3), (0, 2), (1, 2), (2, 2), (0, 1), (1, 1), (2, 1),  (0, 0), (1, 0), (2, 0), (2, 3)] # (x, y), last element is A
    pos = number2coordinate[-1] # starts at A
    sequence = ""
    for button in list(code):
        if button == "A":
            button = -1
        sequence += find_shortest_path(pos, number2coordinate[int(button)], 3, 4, {(0, 3)}, hyperpameters, is_numberpad=True) + "A"
        pos = number2coordinate[int(button)]
    return sequence

dict = {}
def find_sequence_control_panel(buttons, hyperpameters=(0, 0, 0), lookup=False, shortest_paths=None):
    sequence = []
    pos = button2coordinate["A"]
    for button in buttons:
        if not lookup:
            current_sequence = find_shortest_path(pos, button2coordinate[button], 3, 2, {(0, 0)}, hyperpameters) + "A"
            if (pos, button2coordinate[button]) not in dict:
                dict[(pos, button2coordinate[button])] = []
            dict[(pos, button2coordinate[button])].append(current_sequence)
        else:
            current_sequence = shortest_paths[(pos, button2coordinate[button])]
        sequence.append(current_sequence)
        pos = button2coordinate[button]
    return "".join(sequence)

def main(input, num_directional_keypads=25):
    total = 0
    current_sequences = {}
    for code in input.splitlines():
        min_sequence = " " * 10000000
        best_hyperparameter = None
        hyperpameters = [(0, 0, 0)]
        for _ in range(300):
            hyperpameters.append((random.randint(0, 10), random.randint(-10, 3), random.randint(-3, 0)))
        for hyperpameter in hyperpameters:
            sequence = find_sequence_number_pad(code, hyperpameter)
            for i in range(2):
                sequence = find_sequence_control_panel(sequence, hyperpameter)
            if len(sequence) < len(min_sequence):
                min_sequence = sequence
                best_hyperparameter = hyperpameter
        print(best_hyperparameter)
        current_sequences[code] = min_sequence
        total += len(min_sequence)*int(code[:-1])

    shortest_paths = {}
    for key in dict:
        count_dict = {}
        for ele in dict[key]:
            count_dict[ele] = count_dict.get(ele, 0) + 1
        max_cnt = -1
        arg_max = None
        for ele in count_dict:
            if count_dict[ele] > max_cnt:
                max_cnt = count_dict[ele]
                arg_max = ele
        shortest_paths[key] = arg_max
        print(key, arg_max)

    for code in input.splitlines():
        sequence = current_sequences[code]
        for i in range(3):
            #print(i + 2, len(sequence))
            sequence = find_sequence_control_panel(sequence, lookup=True, shortest_paths=shortest_paths)
        length_sequence = len(sequence)
        for j in range(len(sequence) - 1):
            tmp = sequence[j:j+2]
            for _ in range(num_directional_keypads - 5):
                #print(i + 7, length_sequence)
                length_sequence += len(find_sequence_control_panel(tmp, lookup=True, shortest_paths=shortest_paths))
        total += length_sequence * int(code[:-1])
        print(f"{code}:")
        print(length_sequence, int(code[:-1]))

    print(f"Sum of complexities: {total}")


with open("inputs/day21", "r") as file:
    input = file.read()
main(input)

# part 1 best:
# 82, 74, 70, 78, 76
# 74, 74, 70, 72, 76
# 74, 74, 66, 72, 72
# 74, 74, 66, 72, 70

# hyperparameters:
# (9, -4, 0), (4, -4, 0), (10, 6, -5), (7, 4, -1), (2, -2, -1)
# (8, -2, 0), (5, -4, 0), (10, 3, -3), (5, -1, 0), (3, -3, -2)
# (10, -4, 0), (4, -3, 0), (4, -3, -1), (4, -2, 0), (1, 0, -1)

"""
129A:
113463 129
176A:
113400 176
985A:
102564 985
170A:
108486 170
528A:
104811 528
"""
