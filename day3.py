import re

def get_mult_result(str):
    str = str[4:len(str) - 1]
    nums = str.split(",")
    return int(nums[0]) * int(nums[1])

def main(input):
    sum = 0
    pointer = 0

    while pointer < len(input):
        next_potential_occurence = input.find("mul(", pointer, len(input) - 1)
        if next_potential_occurence == -1:
            return sum
        next_occurence = re.match(r"mul\(([0-9]+,[0-9]+\))", input[next_potential_occurence:])
        if next_occurence is not None:
            pointer = next_potential_occurence + input[next_potential_occurence:].find(next_occurence.group(0)) +\
                       len(next_occurence.group(0))
            sum += get_mult_result(next_occurence.group(0))
            continue
        pointer += 1

    return sum

def find_substr(input, str):
    i = 0
    lst = set()
    while i < len(input):
        if input.find(str, i) >= 0:
            lst.add(input.find(str, i))
            i += len(str)
        else:
            i += 1
    return lst

def create_mask(input_length, on_lst, off_lst):
    mask = [True for _ in range(input_length)]
    flag = True
    for i in range(input_length):
        if i in on_lst:
            flag = True
        elif i in off_lst:
            flag = False
        mask[i] = flag
    return mask

def part2(input):
    sum = 0
    pointer = 0
    mask = create_mask(len(input), find_substr(line, "do()"), find_substr(line, "don't()"))

    while pointer < len(input):
        next_potential_occurence = input.find("mul(", pointer, len(input) - 1)
        if next_potential_occurence == -1:
            return sum

        next_occurence = re.match(r"mul\(([0-9]+,[0-9]+)\)", input[next_potential_occurence:])
        if next_occurence is not None:
            pointer = next_potential_occurence + len(next_occurence.group(0))
            if mask[next_potential_occurence]:
                sum += get_mult_result(next_occurence.group(0))
            continue
        pointer += 1

    return sum

with open('inputs/day3', 'r') as file:
    input = file.read()
total = 0
for line in input.splitlines():
    total += main(line)
print(f"total is: {total}")

total2 = 0
for line in input.splitlines():
    total2 += part2(line)
print(f"total of part 2 is: {total2}")