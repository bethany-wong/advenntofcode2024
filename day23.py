import random
class node:
    def __init__(self, name):
        self.name = name
        self.neighbors = set()

def main(input):
    computers = {}
    for line in input.splitlines():
        node1, node2 = line.split("-")
        if node1 not in computers:
            computers[node1] = node(node1)
        if node2 not in computers:
            computers[node2] = node(node2)
        computers[node1].neighbors.add(node2)
        computers[node2].neighbors.add(node1)
    visited = set()
    sets_of_three = set()
    sets_of_three_chief_historian = set()
    for computer_name in computers:
        computer = computers[computer_name]
        neighbors_lst = list(computer.neighbors)
        for i in range(len(neighbors_lst)):
            for j in range(i + 1, len(neighbors_lst)):
                neighbor_1, neighbor_2 = neighbors_lst[i], neighbors_lst[j]
                if tuple(sorted((computer_name, neighbor_1, neighbor_2))) not in visited:
                    visited.add(tuple(sorted((computer_name, neighbor_1, neighbor_2))))
                    if neighbor_2 in computers[neighbor_1].neighbors and neighbor_1 in computers[neighbor_2].neighbors:
                        sets_of_three.add(tuple(sorted((computer_name, neighbor_1, neighbor_2))))
                        if "t" == computer_name[0] or "t" == neighbor_1[0] or "t" == neighbor_2[0]:
                            sets_of_three_chief_historian.add(tuple(sorted((computer_name, neighbor_1, neighbor_2))))

    parties = []
    keys = list(computers.keys())
    random.shuffle(keys)
    for computer_name in keys:
        joined_party = False
        for party in parties:
            cannot_join = False
            for participant_name in party:
                if not computer_name in computers[participant_name].neighbors or not participant_name in computers[computer_name].neighbors:
                    cannot_join = True
                    break
            if not cannot_join:
                party.add(computer_name)
                joined_party = True
        if not joined_party:
            parties.append({computer_name})
    biggest_party = {"size":0, "password": ""}
    for party in parties:
        if len(party) > biggest_party["size"]:
            biggest_party = {"size":len(party), "password": ",".join(sorted(party))}
    print(f"Part 1: {len(sets_of_three_chief_historian)}\nPart 2: the biggest part has size {biggest_party['size']} and password {biggest_party['password']}")

with open("inputs/day23", "r") as file:
    input = file.read()
main(input)