import os
import hashlib
    # TODO: only hash the start of each large file file; VM disks eat all the ram!



try:
    os.chdir("/")
except PermissionError:
    print("Couldn't enter target directory")

filesums = dict()

for root, dirs, files in os.walk(str(os.getcwd()), "*"):
    for name in files:
        try:
            itempath = os.path.join(root, name)
            try:
                itemsum = hashlib.sha1(open(itempath, 'rb').read()).hexdigest()
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

#print(filesums) # Debug for small tests
os._exit(0)
