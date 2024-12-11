import math
class LinkedList():
    def __init__(self, value, next):
        self.value = int(value)
        self.next = next

def main_bruteforce(input, num_blinks):
    stones_list = [[int(s) for s in input.split(" ")]]
    for i in range(num_blinks):
        print(i, len(stones_list))
        splitted_lists = []
        total = 0
        for stones_index in range(len(stones_list)):
            stones = stones_list[stones_index]
            new_stones = []
            for j in range(len(stones)):
                if stones[j] == 0:
                    stones[j] = 1
                else:
                    num_digits = math.floor(math.log10(stones[j])) + 1
                    if num_digits % 2 == 1:
                        stones[j] *= 2024
                    else:
                        middle = 10 ** (num_digits // 2)
                        left_value = stones[j] // middle  # Integer division to get left part
                        right_value = stones[j] % middle
                        stones[j] = left_value
                        new_stones.append(right_value)
            stones += new_stones
            total += len(stones)
            if len(stones) >= 200000:
                first_half, second_half = stones_list[stones_index][:int(len(stones)/2)], stones_list[stones_index][int(len(stones)/2):]
                stones_list[stones_index] = first_half
                splitted_lists.append(second_half)
        stones_list += splitted_lists
    print(total)

def main(input, num_blinks):
    stones = {}
    for s in input.split(" "):
        stones[int(s)] = stones.get(int(s), 0) + 1

    for _ in range(num_blinks):
        new_stones = {}
        for value in stones:
            count = stones[value]
            if value == 0:
                new_stones[1] = new_stones.get(1, 0) + count
            else:
                num_digits = math.floor(math.log10(value)) + 1
                if num_digits % 2 == 1:
                    new_stones[value*2024] = new_stones.get(value*2024, 0) + count
                else:
                    middle = 10 ** (num_digits // 2)
                    left_value = value // middle  # Integer division to get left part
                    right_value = value % middle
                    new_stones[left_value] = new_stones.get(left_value, 0) + count
                    new_stones[right_value] = new_stones.get(right_value, 0) + count
        stones = new_stones
        print(stones)
    total = 0
    for values in stones:
        total += stones[values]
    print(total)

with open("inputs/day11", "r") as file:
    input = file.read()
main(input,75)