import math

def check_order(rules, nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] in rules and nums[i] in rules[nums[j]]:  # order is wrong
                return [i, j]
    return None

def find_middle(lst):
    return int(lst[math.floor(len(lst)/2)])

def find_correct_order(rules, lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[j] in rules and lst[i] in rules[lst[j]]:  # order is wrong
                while i < j:
                    i_value = lst[i]
                    lst[i] = lst[i+1]
                    lst[i+1] = i_value
                    i += 1
    if check_order(rules, lst) is None:
        return lst
    return find_correct_order(rules, lst)

def main(input):
    rules_updates = input.split("\n\n")

    rules_dict = {}
    for rule in rules_updates[0].splitlines():
       before, after = rule.split("|")
       if before not in rules_dict:
           rules_dict[before] = []
       rules_dict[before].append(after)
    for k in rules_dict:
        print(k, rules_dict[k])

    total1 = 0
    total2 = 0
    for update in rules_updates[1].splitlines():
        nums = update.split(",")
        wrong_indices = check_order(rules_dict, nums)
        if wrong_indices is None:
            total1 += find_middle(nums)
        else:
            total2 += find_middle(find_correct_order(rules_dict, nums))

    print(f"Total of part 1: {total1}")
    print(f"Total of part 2: {total2}")

with open('inputs/day5', 'r') as file:
    input = file.read()
main(input)