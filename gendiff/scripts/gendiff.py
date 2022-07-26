import argparse
from ast import arg
import json


DESCRIPTION = 'Compares two configuration files and shows a difference.'


def generate_diff(file_path1, file_path2):
    with open(file_path1, 'r') as f1, open(file_path2, 'r') as f2:
        first_dict = json.load(f1)
        second_dict = json.load(f2)

    alphabetical_keys = [k for k in first_dict]
    alphabetical_keys += [k for k in second_dict]
    alphabetical_keys = list(set(alphabetical_keys))
    alphabetical_keys = sorted(alphabetical_keys)

    diff_lines = []
    for k in alphabetical_keys:
        if k not in first_dict: # added
            diff_lines.append(f'+{k}: {second_dict[k]}')
            continue
        if k not in second_dict: # removed
            diff_lines.append(f'-{k}: {first_dict[k]}')
            continue
        if first_dict[k] == second_dict[k]: # equal
            diff_lines.append(f'{k}: {first_dict[k]}')
            continue
        if first_dict[k] != second_dict[k]: # changed
            diff_lines.append(f'-{k}: {first_dict[k]}')
            diff_lines.append(f'+{k}: {second_dict[k]}')
            continue
    diff_message = '\n'.join(['\t' + l for l in diff_lines])
    diff_message = '{' + diff_message + '\n}'
    return diff_message


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)

    parser.add_argument('-f', '--format', dest='format', 
                        help='set format of output')

    args = parser.parse_args()

    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
