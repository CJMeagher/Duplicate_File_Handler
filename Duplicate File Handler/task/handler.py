import itertools
import sys
import os
from collections import namedtuple
import hashlib

FileDetails = namedtuple("FileDetails", "path size hash sequence", defaults=["", 0])
SizeGroup = namedtuple("SizeGroup", "size paths")
HashGroup = namedtuple("HashGroup", "hash paths")
args = sys.argv
path_to_sequence_dictionary = dict()
sequence_to_path_dictionary = dict()


def main():
    directory = parse_args()
    file_format = get_file_format()
    reverse = get_sort_order()
    file_list = get_file_list(directory, file_format)

    def by_size(file_details):
        return file_details.size

    file_list.sort(key=by_size, reverse=reverse)
    possible_duplicates = []
    for size, grouped_file_list in itertools.groupby(file_list, by_size):
        grouped_file_list = list(grouped_file_list)
        files = [file_details.path for file_details in grouped_file_list]
        if len(files) > 1:
            show_size_group(SizeGroup(size, files))
            new_grouped_file_list = []
            for file_details in grouped_file_list:
                try:
                    with open(file_details.path, "rb") as byte_stream:
                        a_hash = hashlib.md5(byte_stream.read()).hexdigest()
                except PermissionError:
                    print(f"PermissionError: {file_details.path}")
                new_grouped_file_list.append(
                    FileDetails(file_details.path, file_details.size, a_hash)
                )
            possible_duplicates.append(new_grouped_file_list)

    if possible_duplicates:
        pass
    else:
        quit()

    if duplicate_check():
        pass
    else:
        quit()

    def by_hash(file_details):
        return file_details.hash

    for grouped_file_list in possible_duplicates:
        previous_size = 0
        grouped_file_list.sort(key=by_hash)
        for a_hash, files in itertools.groupby(grouped_file_list, by_hash):
            file_list = list(files)
            if len(file_list) > 1:
                current_size = os.path.getsize(file_list[0].path)
                if current_size != previous_size:
                    print()
                    print(f"{str(current_size)} bytes")
                    previous_size = current_size

                paths = [file_details.path for file_details in file_list]
                for path in paths:
                    path_to_sequence_dictionary[path] = (
                        len(path_to_sequence_dictionary) + 1
                    )
                show_hash_group(HashGroup(a_hash, paths))

    sequence_to_path_dictionary.update(
        dict((v, k) for k, v in path_to_sequence_dictionary.items())
    )

    files_to_delete = delete_check()
    if files_to_delete:
        pass
    else:
        quit()

    freed_space = 0
    for file_number in files_to_delete:
        a_path = sequence_to_path_dictionary[file_number]
        freed_space += os.path.getsize(a_path)
        os.remove(a_path)

    print(f"Total freed up space: {freed_space} bytes")


def get_file_list(directory, file_format):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            extension = os.path.splitext(name)[1][1:].lower()
            if file_format == "" or file_format == extension:
                a_path = os.path.join(root, name)
                file_list.append(FileDetails(a_path, os.path.getsize(a_path)))
    return file_list


def show_size_group(a_size_group):
    print()
    print(f"{a_size_group.size} bytes")
    for path in a_size_group.paths:
        print(path)
    print()


def show_hash_group(a_hash_group):
    print(f"Hash: {a_hash_group.hash}")
    for path in a_hash_group.paths:
        print(f"{path_to_sequence_dictionary[path]}. {path}")
    print()


def parse_args():
    try:
        return args[1]
    except IndexError:
        print("Directory is not specified")
        quit()


def get_file_format():
    file_format = input("Enter file format:\n")
    return file_format.lower()


def get_sort_order():
    print("Size sorting options:\n1. Descending\n2. Ascending\n")
    while True:
        try:
            sort_order = input("Enter a sorting option:\n")
            if sort_order == "1":
                return True
            elif sort_order == "2":
                return False
            else:
                raise ValueError
        except ValueError:
            print("Wrong option")


def duplicate_check():
    while True:
        try:
            do_check = input("Check for duplicates?\n").lower()
            if do_check == "yes":
                return True
            elif do_check == "no":
                return False
            else:
                raise ValueError
        except ValueError:
            print("Wrong option")


def delete_check():
    while True:
        try:
            do_check = input("Delete files?\n").lower()
            if do_check == "yes":
                break
            elif do_check == "no":
                return False
            else:
                raise ValueError
        except ValueError:
            print("Wrong option")
    while True:
        try:
            file_numbers_input = input("Enter file numbers to delete:\n").lower()
            file_numbers = [int(x) for x in file_numbers_input.split()]
            if len(file_numbers) == 0:
                raise ValueError
            for number in file_numbers:
                if number not in sequence_to_path_dictionary:
                    raise ValueError
            return file_numbers
        except ValueError:
            print("Wrong format")


main()
