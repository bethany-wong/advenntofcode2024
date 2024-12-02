def check_safety(report):
    increase_flag = report[1] > report[0]
    for i in range(1, len(report)):
        if report[i] >= report[i-1] + 1 and report[i] <= report[i-1] + 3:
            if increase_flag:
                continue
        elif report[i] <= report[i-1] - 1 and report[i] >= report[i-1] - 3:
            if not increase_flag:
                continue
        return False
    return True

def check_safety_with_tolerance(report): # part 2
    for i in range(len(report)):
        if check_safety(report[:i] + report[i + 1:]):
            return True
    return False

def main(input):
    safe_reports_count = 0
    safe_reports_with_tolerance_count = 0

    for line in input.splitlines():
        report_str = line.split(" ")
        report = [int(report_str[i]) for i in range(len(report_str))]
        if check_safety(report):
            safe_reports_count += 1
            safe_reports_with_tolerance_count += 1
        elif check_safety_with_tolerance(report):
            safe_reports_with_tolerance_count += 1

    print(f"Number of safe reports: {safe_reports_count}")
    print(f"Number of safe reports with tolerance: {safe_reports_with_tolerance_count}")


with open('inputs/day2', 'r') as file:
    input = file.read()
maps = main(input)