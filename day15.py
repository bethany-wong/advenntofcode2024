directions = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}

def is_in_map(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def visualise(boxes, walls, robot_position):
    for i in range(len(boxes)):
        row = []
        for j in range(len(boxes[0])):
            if robot_position == (i, j):
                row.append("@")
                continue
            if boxes[i][j]:
                row.append("O")
            elif walls[i][j]:
                row.append("#")
            else:
                row.append(".")
        print(row)

def visualise_part2(boxes_left, boxes_right, walls, robot_position):
    for i in range(len(walls)):
        row = []
        for j in range(len(walls[0])):
            if robot_position == (i, j):
                row.append("@")
                continue
            if boxes_left[i][j]:
                row.append("[")
            elif boxes_right[i][j]:
                row.append("]")
            elif walls[i][j]:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))

def can_move_boxes(current_box, direction, boxes_left, boxes_right, walls): # given left edge of current box
    i, j = current_box
    new_left = (i + direction[0], j + direction[1])
    new_right = (i + direction[0], j + 1 + direction[1])
    if not is_in_map(new_left[0], new_left[1], walls) or walls[new_left[0]][new_left[1]] or not is_in_map(new_right[0], new_right[1], walls) or walls[new_right[0]][new_right[1]]:
        return False
    for pos in [new_left, new_right]:
        if boxes_left[pos[0]][pos[1]]:
            if not can_move_boxes(pos, direction, boxes_left, boxes_right, walls):
                return False
        elif boxes_right[pos[0]][pos[1]]:
            if not can_move_boxes((pos[0], pos[1] - 1), direction, boxes_left, boxes_right, walls):
                return False
    return True

def move_boxes(current_box, direction, boxes_left, boxes_right):
    i, j = current_box
    new_left = (i + direction[0], j + direction[1])
    new_right = (i + direction[0], j + 1 + direction[1])
    if not boxes_left[new_left[0]][new_left[1]] and not boxes_right[new_left[0]][new_left[1]] and not boxes_left[new_right[0]][new_right[1]] and not boxes_right[new_right[0]][new_right[1]]:
        boxes_left[i][j] = False
        boxes_right[i][j+1] = False
        boxes_left[new_left[0]][new_left[1]] = True
        boxes_right[new_right[0]][new_right[1]] = True
        return boxes_left, boxes_right
    for pos in [new_left, new_right]:
        if boxes_left[pos[0]][pos[1]]:
            boxes_left, boxes_right = move_boxes(pos, direction, boxes_left, boxes_right)
        elif boxes_right[pos[0]][pos[1]]:
            boxes_left, boxes_right = move_boxes((pos[0], pos[1] - 1), direction, boxes_left, boxes_right)
    boxes_left[i][j] = False
    boxes_right[i][j + 1] = False
    boxes_left[new_left[0]][new_left[1]] = True
    boxes_right[new_right[0]][new_right[1]] = True
    return boxes_left, boxes_right


def move_part2(robot_position, direction, walls, boxes_left, boxes_right):
    new_i, new_j = robot_position[0] + direction[0], robot_position[1] + direction[1]
    if not is_in_map(new_i, new_j, walls) or walls[new_i][new_j]:
        return robot_position, boxes_left, boxes_right
    if not boxes_left[new_i][new_j] and not boxes_right[new_i][new_j]:
        return (new_i, new_j), boxes_left, boxes_right

    if direction[0] == 0: # horizontal movement
        pointer_j = new_j
        has_space = False
        while is_in_map(new_i, pointer_j, walls):
            if boxes_left[new_i][pointer_j] or boxes_right[new_i][pointer_j]:
                pointer_j += direction[1]
            elif walls[new_i][pointer_j]:
                break
            else:
                has_space = True
                break
        if has_space:
            last = "."
            for j in range(new_j, pointer_j, 1 if pointer_j > new_j else -1):
                current = "[" if boxes_left[new_i][j] else "]"
                if last == ".":
                    boxes_right[new_i][j] = False
                    boxes_left[new_i][j] = False
                elif last == "[":
                    boxes_left[new_i][j] = True
                    boxes_right[new_i][j] = False
                elif last == "]":
                    boxes_left[new_i][j] = False
                    boxes_right[new_i][j] = True
                last = current
            if last == "[":
                boxes_left[new_i][pointer_j] = True
            else:
                boxes_right[new_i][pointer_j] = True
            return (new_i, new_j), boxes_left, boxes_right
        else:
            return robot_position, boxes_left, boxes_right

    has_space = can_move_boxes((new_i, new_j) if boxes_left[new_i][new_j] else (new_i, new_j - 1), direction, boxes_left, boxes_right, walls)
    if has_space:
        boxes_left, boxes_right = move_boxes((new_i, new_j) if boxes_left[new_i][new_j] else (new_i, new_j - 1), direction, boxes_left, boxes_right)
        return (new_i, new_j), boxes_left, boxes_right
    return robot_position, boxes_left, boxes_right

def part2(input):
    map_raw, moves_raw = input.split("\n\n")
    new_map = []
    for line in map_raw.splitlines():
        row = ""
        for j in range(len(line)):
            if line[j] == "#":
                row += "##"
            elif line[j] == "O":
                row += "[]"
            elif line[j] == "@":
                row += "@."
            else:
                row += ".."
        new_map.append(list(row))
    height, width = len(new_map), len(new_map[0])
    walls = [[False for _ in range(width)] for _ in range(height)]
    boxes_left = [[False for _ in range(width)] for _ in range(height)]
    boxes_right = [[False for _ in range(width)] for _ in range(height)]
    robot_position = None
    for i in range(height):
        for j in range(width):
            element = new_map[i][j]
            if element == "#":
                walls[i][j] = True
            elif element == "[":
                boxes_left[i][j] = True
            elif element  == "]":
                boxes_right[i][j] = True
            elif element == "@":
                robot_position = (i, j)
    for line in moves_raw.splitlines():
        for dir in list(line):
            robot_position, boxes_left, boxes_right = move_part2(robot_position, directions[dir], walls, boxes_left, boxes_right)
            #print(f"Move {dir}:")
            #visualise_part2(boxes_left, boxes_right, walls, robot_position)
    gps_total = 0
    for i in range(height):
        for j in range(width):
            if boxes_left[i][j]:
                gps_total += 100 * i + j
    print(f"Sum of all GPS coordinates: {gps_total}")

def move(robot_position, direction, walls, boxes):
    new_i, new_j = robot_position[0] + direction[0], robot_position[1] + direction[1]
    if not is_in_map(new_i, new_j, walls) or walls[new_i][new_j]:
        return robot_position, boxes
    if not boxes[new_i][new_j]:
        return (new_i, new_j), boxes

    pointer_i, pointer_j = new_i,new_j
    has_space = False
    while is_in_map(pointer_i, pointer_j, boxes):
        if boxes[pointer_i][pointer_j]:
            pointer_i += direction[0]
            pointer_j += direction[1]
        elif walls[pointer_i][pointer_j]:
            break
        else:
            has_space = True
            break
    if has_space:
        boxes[new_i][new_j] = False
        boxes[pointer_i][pointer_j] = True
        return (new_i, new_j), boxes
    return robot_position, boxes

def main(input):
    map_raw, moves_raw = input.split("\n\n")
    max_row, max_col = len(map_raw.splitlines()), len(map_raw.splitlines()[0])
    walls = [[False for _ in range(max_col)] for _ in range(max_row)]
    boxes = [[False for _ in range(max_col)] for _ in range(max_row)]
    robot_position = None
    row_cnt = 0
    for line in map_raw.splitlines():
        for j in range(len(line)):
            if line[j] == "#":
                walls[row_cnt][j] = True
            elif line[j] == "O":
                boxes[row_cnt][j] = True
            elif line[j] == "@":
                robot_position = (row_cnt, j)
        row_cnt += 1
    for line in moves_raw.splitlines():
        for dir in list(line):
            robot_position, boxes = move(robot_position, directions[dir], walls, boxes)
            #print(f"Move {dir}:")
            #visualise(boxes, walls, robot_position)
    gps_total = 0
    for i in range(max_row):
        for j in range(max_col):
            if boxes[i][j]:
                gps_total += 100 * i + j
    print(f"Sum of all GPS coordinates: {gps_total}")


with open("inputs/day15", "r") as file:
    input = file.read()
main(input)
part2(input)