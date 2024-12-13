def find_min_tokens(machine):
    x_a, y_a = machine["buttons"]["A"]
    x_b, y_b = machine["buttons"]["B"]
    prize_x, prize_y = machine["prize"]
    numerator = prize_y/y_a - prize_x/x_a
    denominator = y_b/y_a - x_b/x_a
    b = round(numerator / denominator)
    a = (prize_x - b*x_b)/x_a
    if int(a) * x_a + int(b) * x_b == prize_x and int(a) * y_a + int(b) * y_b == prize_y:
        return int(a), int(b)
    return -1, -1

def main(input, part_2=False):
    machines = []
    for machine_str in input.split("\n\n"):
        lines = machine_str.splitlines()
        xy_a = lines[0].split(": ")[1].split(", ")
        xy_b = lines[1].split(": ")[1].split(", ")
        xy_prize = lines[2].split(": ")[1].split(", ")
        machine = {"buttons":{"A":(int(xy_a[0].split("+")[1]), int(xy_a[1].split("+")[1])),
                              "B":(int(xy_b[0].split("+")[1]), int(xy_b[1].split("+")[1]))},
                   "prize":(int(xy_prize[0].split("=")[1]) + (10000000000000 if part_2 else 0), int(xy_prize[1].split("=")[1]) + (10000000000000 if part_2 else 0))}
        machines.append(machine)
    total = 0
    for machine in machines:
        tokens_a, tokens_b = find_min_tokens(machine)
        total += tokens_a * 3 + tokens_b * 1 if tokens_a != -1 else 0
    print(f"Fewest tokens to win all possible prizes: {total}")

with open("inputs/day13", "r") as file:
    input = file.read()
main(input)
main(input, True)