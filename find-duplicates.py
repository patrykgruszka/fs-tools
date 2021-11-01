import glob
import os
import argparse
from imohash import hashfile


def get_files_info(filenames):
    files_list = []
    hash_list = []

    for filepath in filenames:
        if not os.path.isdir(filepath):
            checksum = hashfile(filepath, hexdigest=True)

            file_info = {
                'path': filepath,
                'checksum': checksum
            }
            files_list.append(file_info)
            hash_list.append(checksum)

    return files_list, hash_list


parser = argparse.ArgumentParser(description='This script finds duplicated files in directory')
parser.add_argument("path", nargs="+", help="Directory to search")
parser.add_argument('-r', '--recursive', action='store_true', default=False, help='Search through subfolders')

args = parser.parse_args()

for path in args.path:
    if not os.path.isdir(path):
        raise NotADirectoryError(path)

all_files_list = []
all_files_hashes = []

for path in args.path:
    if args.recursive:
        filenames = glob.glob(path + "/**/*", recursive=True)
    else:
        filenames = glob.glob(path + "/*")

    files_list, hash_list = get_files_info(filenames)
    all_files_list += files_list
    all_files_hashes += hash_list

seen = set()
duplicated_hashes = [x for x in all_files_hashes if x in seen or seen.add(x)]

for checksum in duplicated_hashes:
    for file in all_files_list:
        if checksum == file['checksum']:
            print(file['path'])
