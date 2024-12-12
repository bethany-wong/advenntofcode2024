from collections import defaultdict

def is_in_map(i, j, map):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[0])

def contains(i, j, garden_plot, regions):
    if not garden_plot in regions:
        return False
    for region in regions[garden_plot]:
        if (i, j) in region:
            return True
    return False

def floodfill(i, j, garden_plot, map, lst, visited):
    if not is_in_map(i, j, map) or visited[i][j]:
        return lst
    visited[i][j] = True
    if map[i][j] != garden_plot:
        return lst
    lst.add((i, j))
    for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        new_i, new_j = i + direction[0], j + direction[1]
        lst = floodfill(new_i, new_j, garden_plot, map, lst, visited)
    return lst

def calculate_perimeter(lst):
    perimeter = len(lst) * 4
    for i in range(len(lst)-1):
        for j in range(i+1, len(lst)):
            i_row, i_col = lst[i]
            j_row, j_col = lst[j]
            for direction in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                if i_row + direction[0] == j_row and i_col+ direction[1] == j_col:
                    perimeter -= 2
                    break
    return perimeter

def is_corner(a, b):
    intersection = set(a).intersection(set(b))
    if len(intersection) != 1:
        return None
    if a[0][0] == a[1][0] == b[0][0] == b[1][0] or a[0][1] == a[1][1] == b[0][1] == b[1][1]:
        return None
    return intersection

def find_outer_edges(lst):
    edge_map = {
        (0, 1): [[0, 1], [1, 1]],
        (1, 0): [[1, 1], [1, 0]],
        (0, -1): [[0, 0], [1, 0]],
        (-1, 0): [[0, 0], [0, 1]]
    }
    edges = set()
    for vertex in lst: # find all edges
        for side in [[[0, 0], [0, 1]], [[0, 1], [1, 1]], [[1, 1], [1, 0]], [[1, 0], [0, 0]]]:
            edges.add((tuple(sorted([(vertex[0] + side[0][0], vertex[1] + side[0][1]), (vertex[0] + side[1][0], vertex[1] + side[1][1])]))))
    for i in range(len(lst)-1): # remove inner edges
        for j in range(i+1, len(lst)):
            i_row, i_col = lst[i]
            j_row, j_col = lst[j]
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if i_row + direction[0] == j_row and i_col+ direction[1] == j_col:
                    edge_a, edge_b = (i_row + edge_map[direction][0][0], i_col + edge_map[direction][0][1]), (i_row + edge_map[direction][1][0], i_col + edge_map[direction][1][1])
                    edges.remove(tuple(sorted([edge_a, edge_b])))
                    break
    return edges

def find_sides(edges):
    horizontal_edges = defaultdict(list)
    vertical_edges = defaultdict(list)
    for edge in edges:
        a_row, a_col = edge[0]
        b_row, b_col = edge[1]
        if a_row == b_row:
            horizontal_edges[a_row].append(tuple(sorted([a_col, b_col])))
        else:
            vertical_edges[a_col].append(tuple(sorted([a_row, b_row])))
    corners_count = 0
    points = defaultdict(int)
    edges = list(edges)
    for i in range(len(edges) - 1):
        for j in range(i+1, len(edges)):
            point = is_corner(edges[i], edges[j])
            if point is not None:
                point = tuple(list(point))
                if points[point] < 2:
                    points[point] += 1
                    corners_count += 1
    return corners_count

def main(input):
    map = []
    row_cnt = 0
    for line in input.splitlines():
        row = []
        for col in range(len(line)):
            row.append(line[col])
        map.append(row)
        row_cnt += 1
    col_cnt = len(map[0])

    regions = defaultdict(list)
    for i in range(row_cnt):
        for j in range(col_cnt):
            garden_plot = map[i][j]
            if contains(i, j, garden_plot, regions):
                continue
            regions[garden_plot].append(list(floodfill(i, j, garden_plot, map, set(), [[False for _ in range(col_cnt)] for _ in range(row_cnt)])))

    total = 0
    total_part2 = 0
    for plant in regions:
        for region in regions[plant]:
            outer_edges = find_outer_edges(region)
            corners = find_sides(outer_edges)
            print(plant, len(region), corners)
            total += len(region) * calculate_perimeter(region)
            total_part2 += len(region) * corners
    print(f"Total price: {total}; Part 2 total price: {total_part2}")

with open("inputs/day12", "r") as file:
    input = file.read()
main(input)