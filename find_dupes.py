import argparse
import os
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument("target_path", help="- base path to recursively search")
args = parser.parse_args()

target_directory = args.target_path

try:
    os.chdir(target_directory)
except PermissionError:
    print("Couldn't enter target directory")
    os._exit(2)
except FileNotFoundError:
    print("Couldn't find requested path")
    os._exit(3)

filesums = dict()
itempath = ""

for root, dirs, files in os.walk(str(os.getcwd()), "*"):
    for name in files:
        try:
            itempath = os.path.join(root, name)
            try:
                '''
                Instead of reading in the whole file, just read up to the 1st megabyte of the file; should be plenty
                Hash that first 1MB and look for the hash as an existing key, if it's not in there, the file in question
                is not a duplicate file.
                '''
                itemsum = hashlib.sha1(open(itempath, 'rb').read(1000000)).hexdigest()
                if itemsum in filesums:
                    print("Found duplicate file checksum: " + itemsum + " in both: " + itempath + " and in: " + filesums[itemsum])

                # Add new item to dictionary
                filesums[itemsum] = itempath
            # Dodge symlinks, sockets etc
            except (FileNotFoundError, OSError):
                print("Skipping problematic file: " + itempath)
                pass
            except MemoryError:
                print("Whoops ate all the RAM...")
                pass
        # Accept that there may be files we can't access
        except PermissionError:
            print("Hit permissions problem on: " + itempath)
            pass

os._exit(0)
