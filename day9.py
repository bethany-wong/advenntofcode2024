def calculate_checksum(filesystem):
    sum = 0
    for i in range(len(filesystem)):
        if filesystem[i] != ".":
            sum += int(filesystem[i]) * i
    print(f"Resulting filesystem checksum is: {sum}")

def part1(filesystem):
    left, right = 0, len(filesystem) - 1
    while left < right:
        if filesystem[left] != ".":
            left += 1
            continue
        if filesystem[right] == ".":
            right -= 1
            continue
        filesystem[left] = filesystem[right]
        filesystem[right] = "."
        left += 1
        right -= 1
    return filesystem

def find_space(filesystem, length, end):
    template = ["." for _ in range(length)]
    for i in range(end):
        if filesystem[i:i+length] == template:
            return i
    return -1

def part2(filesystem):
    id = filesystem[-1]
    while int(id) >= 0:
        start_index = -1
        end_index = -1
        for i in range(len(filesystem)):
            if filesystem[i] == id:
                if start_index == -1:
                    start_index = i
                    end_index = i
                else:
                    end_index = i
        required_space = (end_index - start_index + 1)
        space_start = find_space(filesystem, required_space, start_index)
        if space_start != -1:
            for i in range(required_space):
                filesystem[space_start + i] = filesystem[start_index + i]
                filesystem[start_index + i] = "."
        id = str(int(id) - 1)
    return filesystem

def convert_to_str(input):
    filesystem = []
    filesystem_index = 0
    is_file = True
    for i in range(len(input)):
        filesystem += [str(int(i / 2)) if is_file else "." for _ in range(int(input[i]))]
        is_file = not is_file
        filesystem_index += int(input[i])
    return filesystem

def convert_to_str_from_dict(input):
    filesystem = []
    for element in input:
        filesystem += [str(element["value"]) if element["is_file"] else "." for _ in range(element["count"])]
    return filesystem

with open("inputs/day9", "r") as file:
    input = file.read()
calculate_checksum(part1(convert_to_str(input)))
calculate_checksum(part2(convert_to_str(input)))