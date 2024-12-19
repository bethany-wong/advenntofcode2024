import math


def run_program(A, B, C, program):
    outputs = []
    ip = 0
    while ip < len(program):
        instruction, literal_operand = program[ip], program[ip + 1]
        combo_operand = literal_operand
        if combo_operand == 4:
            combo_operand = A
        elif combo_operand == 5:
            combo_operand = B
        elif combo_operand == 6:
            combo_operand = C

        if instruction == 0:  # adv
            A = int(A / 2 ** combo_operand)
        elif instruction == 1:  # bxl
            B ^= literal_operand
        elif instruction == 2:  # bst
            B = combo_operand % 8
        elif instruction == 3:  # jnz
            if A != 0:
                ip = literal_operand
                continue
        elif instruction == 4:  # bxc
            B ^= C
        elif instruction == 5:  # out
            outputs.append(str(combo_operand % 8))
        elif instruction == 6:  # bdv
            B = int(A / 2 ** combo_operand)
        elif instruction == 7:  # cdv
            C = int(A / 2 ** combo_operand)
        ip += 2
    return outputs

def main(input):
    register_values, program = input.split('\n\n')
    register_values = register_values.splitlines()
    program = program.split(': ')[1].split(',')
    program = [int(element) for element in program]
    A, B, C = [int(register_values[i].split(': ')[1]) for i in range(len(register_values))]
    print('Part 1:\n' + ','.join(run_program(A, B, C, program)))

with open("inputs/day17", "r") as file:
    input = file.read()
main(input)