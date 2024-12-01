import copy
import math
import sys

def find_next(num, map, max):
    while num < max:
        if num in map:
            break
        num += 1
    return num

def main(input):
    min = [sys.maxsize, sys.maxsize]
    max = [-sys.maxsize, -sys.maxsize]
    maps = [{}, {}]

    for line in input.splitlines():
        nums = line.split("   ")
        nums = [int(nums[0]), int(nums[1])]
        for i in range(2):
            if nums[i] < min[i]:
                min[i] = nums[i]
            if nums[i] > max[i]:
                max[i] = nums[i]
            if nums[i] in maps[i]:
                maps[i][nums[i]] += 1
            else:
                maps[i][nums[i]] = 1

    maps_copy = copy.deepcopy(maps)

    distance = 0
    pointer = min
    for i in range(len(input.splitlines())):
        distance += math.fabs(pointer[0] - pointer[1])
        for j in range(2):
            if maps[j][pointer[j]] == 1:
                del maps[j][pointer[j]]
            else:
                maps[j][pointer[j]] -= 1
            pointer[j] = find_next(pointer[j], maps[j], max[j])

    print(int(distance))
    return maps_copy

# -------------------- part 2 ----------------------------
def part2(maps):
    similarity = 0
    for key in maps[0]:
        if key in maps[1]:
            similarity += key * maps[0][key] * maps[1][key]
            print(key, maps[0][key], maps[1][key])
    print("Similarity score: " + str(similarity))


with open('inputs/day1', 'r') as file:
    input = file.read()
maps = main(input)
part2(maps)