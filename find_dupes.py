#!/usr/bin/python3
#


import argparse
import os
import sys
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument("target_path", help="- base path to recursively search")
args = parser.parse_args()

target_directory = args.target_path

try:
    os.chdir(target_directory)
except PermissionError:
    print("Couldn't enter target directory")
    sys.exit(2)
except FileNotFoundError:
    print("Couldn't find requested path")
    sys.exit(3)

file_checksums = dict()
item_path = ""

for root, dirs, files in os.walk(str(os.getcwd()), "*"):
    for name in files:
        try:
            item_path = os.path.join(root, name)
            try:
                '''
                Instead of reading in the whole file, just read up to the 1st megabyte of the file; should be plenty
                Hash that first 1MB and look for the hash as an existing key, if it's not in there, the file in question
                is not a duplicate file.
                '''
                item_checksum = hashlib.sha1(open(item_path, 'rb').read(1000000)).hexdigest()
                if item_checksum in file_checksums:
                    print(
                        "Found duplicate file checksum: " + item_checksum + " " + item_path +
                        " " + file_checksums[item_checksum]
                    )

                # Add new item to dictionary
                file_checksums[item_checksum] = item_path
            # Dodge symlinks, sockets etc
            except (FileNotFoundError, OSError):
                print("Skipping problematic file: " + item_path)
                pass
            except MemoryError:
                print("Whoops ate all the RAM...")
                pass
        # Accept that there may be files we can't access
        except PermissionError:
            print("Hit permissions problem on: " + item_path)
            pass

sys.exit(0)
