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


parser = argparse.ArgumentParser(description='This script compares files in two directories and returns the diff')
parser.add_argument("--dir1", dest="dir1", help="first directory path to compare")
parser.add_argument("--dir2", dest="dir2", help="second directory path to compare")

args = parser.parse_args()

if not args.dir1 or not args.dir2:
    parser.error('--dir1 and --dir2 parameters are required')

dir1_filenames = glob.glob(args.dir1, recursive=True)
dir1_file_list, dir1_hash_list = get_files_info(filenames=dir1_filenames)

dir2_file_names = glob.glob(args.dir2, recursive=True)
dir2_file_list, dir2_hash_list = get_files_info(filenames=dir2_file_names)

difference = list(set(dir2_hash_list) - set(dir1_hash_list))

diff_files = []
for diff_checksum in difference:
    diff_file = next((item for item in dir2_file_list if item["checksum"] == diff_checksum), None)
    if diff_file:
        diff_files.append(diff_file)
        print(diff_file['path'])
