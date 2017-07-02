import os
import hashlib



try:
    os.chdir("/home/freeos/logs")
except PermissionError:
    print("Couldn't enter target directory")

filesums = dict()

for root, dirs, files in os.walk(str(os.getcwd()), "*"):
    for name in files:
        try:
            itempath = os.path.join(root, name)
            try:
                itemsum = hashlib.sha1(open(itempath, 'rb').read()).hexdigest()

                # Add new item to dictionary
                filesums[itemsum] = itempath
            # Dodge symlinks, sockets etc
            except (FileNotFoundError, OSError):
                print("Skipping problematic file: " + itempath)
                pass
            #if itemsum in filesums:
            #    print("Found duplicate file checksum " + itemsum + "in both " + itempath " and in " filesums[itemsum])
        # Accept that there may be files we can't access
        except PermissionError:
            print("Hit permissions problem on: " + itempath)
            pass

print(filesums)
os._exit(0)
