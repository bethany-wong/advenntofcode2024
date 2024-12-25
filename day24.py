import copy
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def perform_bitwise_operation(arg1, arg2, operator):
    if operator == "AND":
        return arg1 & arg2
    if operator == "OR":
        return arg1 | arg2
    if operator == "XOR":
        return arg1 ^ arg2

def visualise(input_gates, intermediate_gates, output_gates, gates):
    G = nx.DiGraph()

    for i in sorted(input_gates):
        gate = gates[i]
        G.add_edge(gate['input'][0], gate['output'], label=gate['operator'])
        G.add_edge(gate['input'][1], gate['output'], label=gate['operator'])

    for i in sorted(intermediate_gates):
        gate = gates[i]
        G.add_edge(gate['input'][0], gate['output'], label=gate['operator'])
        G.add_edge(gate['input'][1], gate['output'], label=gate['operator'])

    for i in sorted(output_gates):
        gate = gates[i]
        G.add_edge(gate['input'][0], gate['output'], label=gate['operator'])
        G.add_edge(gate['input'][1], gate['output'], label=gate['operator'])

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_labels = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_labels,
        textposition='top center',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='lightblue',
            size=10,
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    fig.show()

def main(input, part1=True):
    configs, gates_raw = input.split("\n\n")
    states = {}
    gates = []
    for line in configs.splitlines():
        wire, value = line.split(": ")
        states[wire] = int(value)
    for line in gates_raw.splitlines():
        rest, output = line.split(" -> ")
        gate = rest.split(" ")
        gates.append({"input": (gate[0], gate[2]), "operator": gate[1], "output": output, "processed": False})

    finished = False
    while not finished:
        finished = True
        for gate in gates:
            if gate["processed"] == False:
                finished = False
                if gate["input"][0] in states and gate["input"][1] in states:
                    states[gate["output"]] = perform_bitwise_operation(states[gate["input"][0]], states[gate["input"][1]], gate["operator"])
                    gate["processed"] = True

    # ------------------------------ part 2 ------------------------------------------
    input_gates, output_gates, intermediate_gates = [], [], []
    for i in range(len(gates)):
        gate = gates[i]
        if gate["input"][0][0] == "x" or gate["input"][0][0] == "y" and gate["input"][1][0] == "x" or gate["input"][1][0] == "y":
            input_gates.append(i)
        if gate["output"][0] == "z":
            output_gates.append(i)
        if not (gate["input"][0][0] == "x" or gate["input"][0][0] == "y" and gate["input"][1][0] == "x" or gate["input"][1][0] == "y") and gate["output"][0] != "z":
            intermediate_gates.append(i)
    print(f"{len(input_gates)} input gates:")
    print([gates[i] for i in input_gates])
    print(f"{len(output_gates)} output gates:")
    print([gates[i] for i in output_gates])
    print(f"{len(intermediate_gates)} intermediate gates:")
    print([gates[i] for i in intermediate_gates])
    for i in input_gates:
        if i in output_gates:
            print(f"Both input and output gate: {gates[i]}")
    print()

    xy_attention = {}
    for i in range(len(input_gates)):
        current_wire = gates[input_gates[i]]["input"]
        current_output = gates[input_gates[i]]["output"]
        paths = [[current_output]]
        full_paths = []
        while paths:
            current = paths.pop()
            if current[-1][0] == "z":
                if current not in full_paths:
                    full_paths.append(current)
                continue
            tmp = current[-1]
            for j in range(len(gates)):
                if tmp in gates[j]["input"]:
                    current_copy = copy.deepcopy(current)
                    current_copy.append(gates[j]["output"])
                    paths.append(current_copy)
        xy_attention[int(current_wire[0][1:])] = full_paths

    PRINT_ATTENTION = False
    if PRINT_ATTENTION:
        for key in sorted(xy_attention):
            print(f"Wire number {key}, length {len(xy_attention[key])}")
            print(sorted([path[-1] for path in xy_attention[key]]))
            for path in xy_attention[key]:
                print(path)
        print()

    visualise(input_gates, intermediate_gates, output_gates, gates)

    x, y, z = "", "", ""
    for key in sorted(states):
        if key[0] == "x":
            x = str(states[key]) + x
        elif key[0] == "y":
            y = str(states[key]) + y
        elif key[0] == "z":
            z = str(states[key]) + z
    answer = bin(int(x, 2)+int(y, 2))[2:]
    print(f"x:  {x}, {int(x, 2)}\ny:  {y}, {int(y, 2)}\nz: {z}, {int(z, 2)}\n   {answer}, {int(answer, 2)}\n")

    correct_gates = set()
    for i in range(46):
        if z[45-i] != answer[45-i]:
            print(f"z{str(i).zfill(2)}")
            new_gates = set()
            for key in sorted(xy_attention):
                for path in xy_attention[key]:
                    if path[-1] == f"z{str(i).zfill(2)}":
                        for element in path[:-1]:
                            if element not in correct_gates:
                                new_gates.add(element)
            print(len(correct_gates), new_gates)
        else:
            new_gates = set()
            for key in sorted(xy_attention):
                for path in xy_attention[key]:
                    if path[-1] == f"z{str(i).zfill(2)}":
                        new_gates.update(path)
            correct_gates.update(new_gates)


with open("inputs/day24", "r") as file:
    input = file.read()
main(input, part1=False)