def mix_and_prune(num1, num2):
    return (num1 ^ num2) % 2 ** 24

def calculate_next_secret_number(number):
    number = mix_and_prune(number << 6, number)
    number = mix_and_prune(number >> 5, number)
    number = mix_and_prune(number << 11, number)
    return number

def is_in(sublst, lst):
    sublst_str = "".join([str(ele) for ele in sublst])
    lst_str = "".join([str(ele) for ele in lst])
    if sublst_str in lst_str:
        start_index = len(lst_str[:lst_str.index(sublst_str)].replace("-", ""))
        if sublst == lst[start_index:start_index+4]:
            return start_index
    return -1

def is_in_lst(sublst, lst):
    for i in range(len(lst) - len(sublst) + 1):
        if lst[i:i+len(sublst)] == sublst:
            return i
    return -1

def calculate_total_sell_price(sequence, changes, prices):
    sequence = list(sequence)
    total_sell_price = 0
    for buyer_index in range(len(changes)):
        observe_start_index = is_in(sequence, changes[buyer_index])
        if observe_start_index != -1:
            price = prices[buyer_index][observe_start_index + 3]
            total_sell_price += price
    return total_sell_price

def main(input, num_iteration=2000):
    prices, changes = [], []
    total = 0
    for line in input.splitlines():
        current_secret_number = int(line)
        price_lst, changes_lst = [], []
        for i in range(1, num_iteration+1):
            last = current_secret_number % 10
            current_secret_number = calculate_next_secret_number(current_secret_number)
            price_lst.append(current_secret_number % 10)
            changes_lst.append(current_secret_number % 10 - last)
        total += current_secret_number
        prices.append(price_lst)
        changes.append(changes_lst)
    print(f"Part 1: {total}")
    sequence_to_sell_price = {}
    checked_sequences = set()
    max_price = -1
    best_sequence = None
    for i in range(len(prices)):
        print(f"Checking buyer number: {i}")
        for j in range(num_iteration - 3):
            current_sequence = tuple(changes[i][j:j+4])
            if current_sequence not in checked_sequences:
                checked_sequences.add(current_sequence)
                current_price = calculate_total_sell_price(current_sequence, changes, prices)
                sequence_to_sell_price[current_sequence] = current_price
                if current_price > max_price:
                    print(f"Buyer number {i}, start index {j}: updated max price to {current_price} with sequence {current_sequence}")
                    max_price = current_price
                    best_sequence = current_sequence
        print(f"Size of hashed sequences: {len(sequence_to_sell_price)}")
    print(max_price, list(best_sequence))


with open("inputs/day22", "r") as file:
    input = file.read()
main(input)