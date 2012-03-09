import os
import time
import re
import settings

RECSMATCH=0
#RECSREAD=0

pattern = re.compile(settings.TARGET_USERNAME)

with open(settings.BIG_FILE, "r") as fh_in:
    for line in fh_in:
        #RECSREAD += 1
        if pattern.search(line):
            RECSMATCH += 1
            
#print(RECSREAD,RECSMATCH)            
print(RECSMATCH)            
