# Make smaller version of bigfile for testing.
import os
import sys

head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, head)
import settings

outfile ="/home/rhancock/bigmedfile.xferlog"

with open(settings.BIG_FILE, "r") as fin:
    with open(outfile, "w") as fout:
        c = 1
        for line in fin:
            fout.write("{n} {l}".format(n=c, l=line))
            c += 1
            if c > 20000000:
                break