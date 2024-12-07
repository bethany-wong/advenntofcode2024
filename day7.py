def is_combination(running_sum, test_value, nums):
    if len(nums) == 0:
        return running_sum == test_value
    if is_combination(running_sum+nums[0], test_value, nums[1:]) or is_combination(running_sum*nums[0], test_value, nums[1:]):
        return True

def is_combination_part2(running_sum, test_value, nums):
    if len(nums) == 0:
        return running_sum == test_value
    if is_combination_part2(running_sum+nums[0], test_value, nums[1:]) or is_combination_part2(running_sum*nums[0], test_value, nums[1:]) or is_combination_part2(int(str(running_sum) + str(nums[0])), test_value, nums[1:]):
        return True

def main(input):
    total, total2 = 0, 0
    for line in input.splitlines():
        test_value = int(line.split(": ")[0])
        nums = [int(i) for i in line.split(": ")[1].split(" ")]
        total += test_value if is_combination(nums[0], test_value, nums[1:]) else 0
        total2 += test_value if is_combination_part2(nums[0], test_value, nums[1:]) else 0
    print(f"Total calibration result is: {total}\nTotal calibration result for part 2 is: {total2}")

with open("inputs/day7", "r") as file:
    input = file.read()
main(input)