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

def combine_spaces(filesystem):
    pointer = 0
    while(pointer < len(filesystem)):
        if not filesystem[pointer]["is_file"] and pointer+1<len(filesystem) and not filesystem[pointer+1]["is_file"]:
            filesystem[pointer]["count"] += filesystem[pointer + 1]["count"]
            filesystem = filesystem[:pointer + 1] + filesystem[pointer + 2:] if pointer + 2 < len(filesystem) else filesystem[:pointer + 1]
        else:
            pointer += 1
    return filesystem

def part2(input):
    filesystem = []
    for i in range(len(input)):
        if i % 2 == 0:
            filesystem.append({"is_file":True, "count":int(input[i]), "value":int(i/2)})
        else:
            filesystem.append({"is_file": False, "count": int(input[i])})
    i = len(filesystem) - 1
    while i >= 0:
        #print(convert_to_str_dict(filesystem))
        if filesystem[i]["is_file"]:
            required_space = filesystem[i]["count"] * len(str(filesystem[i]["value"]))
            space = -1
            for j in range(i):
                if not filesystem[j]["is_file"] and filesystem[j]["count"] >= required_space:
                        space = j
                        break
            if space > -1:
                filesystem[space]["count"] -= required_space
                i_value = filesystem[i]["value"]
                if i < len(filesystem) - 1:
                    filesystem = filesystem[:space] + [filesystem[i]] + [filesystem[space]] + filesystem[space+1:i] +  [{"is_file": False, "count": required_space}] + filesystem[i+1:]
                else:
                    filesystem = filesystem[:space] + [filesystem[i]] + [filesystem[space]] + filesystem[space+1:i] + [{"is_file": False, "count": required_space}]
                filesystem = combine_spaces(filesystem)
                if i_value == 0:
                    break
                for j in range(len(filesystem)):
                    if filesystem[j]["is_file"] and filesystem[j]["value"] == i_value-1:
                        i = j+1
                        break
        i -= 1
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

def convert_to_str_dict(input):
    filesystem = []
    for element in input:
        filesystem += [str(element["value"]) if element["is_file"] else "." for _ in range(element["count"])]
    return filesystem

with open("inputs/day9", "r") as file:
    input = file.read()
calculate_checksum(part1(convert_to_str(input)))
calculate_checksum(convert_to_str_dict(part2(input)))