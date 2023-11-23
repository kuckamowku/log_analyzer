import argparse
import re
from collections import defaultdict

def parse_log(input_file, keywords, output_file=None, group_by_id=False, id_pattern=None, template=None):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    matched_lines = []
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                if template:
                    line = re.findall(template, line)
                    line = ' '.join(line)
                if len(line) != 0:
                    matched_lines.append(line + '\n')
                break

    if group_by_id and id_pattern:
        groups = defaultdict(list)
        for line in matched_lines:
            id_match = re.search(id_pattern, line)
            if id_match:
                id_value = id_match.group()
                groups[id_value].append(line)

        for id_value, lines in groups.items():
            with open(f"{output_file}_{id_value}.txt", "w", encoding='utf-8') as f:
                f.writelines(lines)
    elif output_file:
        with open(output_file, "w") as f:
            f.writelines(matched_lines)
    else:
        for line in matched_lines:
            print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log parser')
    parser.add_argument('input_file', help='Input log file')
    parser.add_argument('keywords', nargs='+', help='Keywords to search for')
    parser.add_argument('-o', '--output_file', help='Output file for parsed lines')
    parser.add_argument('-g', '--group_by_id', action='store_true', help='Group lines by identifier')
    parser.add_argument('-i', '--id_pattern', help='Identifier pattern (regex)')
    parser.add_argument('-t', '--template', help='Template to cut parts of lines (regex)')

    args = parser.parse_args()
    parse_log(args.input_file, args.keywords, args.output_file, args.group_by_id, args.id_pattern, args.template)