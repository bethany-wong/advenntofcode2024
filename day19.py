def find_prefixes(design, patterns):
    prefixes = []
    for pattern in patterns:
        if design.find(pattern) == 0:
            prefixes.append(pattern)
    return prefixes

checked = {}
def find_combination_recursive(design, patterns):
    if design == '':
        return 1
    prefixes = find_prefixes(design, patterns)
    remaining_str = set()
    for new_str in [design[len(substr):] for substr in prefixes]:
        remaining_str.add(new_str)
    combinations_cnt = 0
    for str in remaining_str:
        if str in checked:
            combinations_cnt += checked[str]
        else:
            combinations_cnt += find_combination_recursive(str, patterns)
    checked[design] = combinations_cnt
    return combinations_cnt

def main(input):
    patterns, designs = input.split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.splitlines()
    total = 0
    total_possible_combinations = 0
    for design in designs:
        num_combinations = find_combination_recursive(design, patterns)
        print(design, num_combinations)
        if num_combinations > 0:
            total += 1
            total_possible_combinations += num_combinations
    print(f'Number of possible towels: {total}\nNumber of combinations: {total_possible_combinations}')

with open("inputs/day19", "r") as file:
    input = file.read()
main(input)