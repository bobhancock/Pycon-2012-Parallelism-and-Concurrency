# Make the first field in bigfile the record number
import os
import sys

head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, head)
import settings
fname = settings.BIG_FILE+"_numbered"
i = 1

with open(settings.BIG_FILE, "r") as fh:
    with open(fname, "w") as fout:
        for line in fh:
            fout.write("{i} {l}".format(i=i, l=line))
            i += 1
                       
print("Done")                       
        