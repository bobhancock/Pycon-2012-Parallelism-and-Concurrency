fname = "/home/rhancock/bigfile.xferlog"
c = 0
with open(fname, "r") as fh:
    for line in fh:
        c += 1
print(c)
