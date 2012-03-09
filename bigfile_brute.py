import os
import time
import settings

#recsread = 0
recsmatch = 0

with open(settings.BIG_FILE, "r") as fh_in:
    for line in fh_in:
        #recsread += 1
        if settings.TARGET_USERNAME in line: # What is the big O of this operation?
            recsmatch += 1

#print("{r} {m}".format(r=recsread, m=recsmatch))
print("{m}".format(m=recsmatch))
