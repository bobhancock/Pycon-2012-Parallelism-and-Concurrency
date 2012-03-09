""" Coroutine version of pipeline. """ 
import os
import sys
import re
import time

import settings
from coroutinedec import coroutine

RECSMATCH=0  #This should be synchronized
#RECSREAD=0

@coroutine
def opener(target_coroutine):
    while True:
        name = (yield)
        print("opener name={n}".format(n=name))
        #if name.endswith(".gz"):
            #f = gzip.open(name)
        #elif name.endswith('.bz2'):
            #f = bz2.BZ2File(name)
        #else:
        f = open(name, "r")
                
        target_coroutine.send(f)
    
            
@coroutine        
def cat(target_coroutine):

    while True:
        f = (yield)
        for line in f:
            #RECSREAD += 1
            target_coroutine.send(line)
            
@coroutine
def grep(pattern, target_coroutine):
    while True:
        line = (yield)
        if pattern.search(line): #change to regex or re2
            target_coroutine.send(line)         

            
@coroutine            
def writer():
    global RECSMATCH
    while True:
        #print("Match")
        line = (yield)
        RECSMATCH += 1

def main():
    pattern = re.compile(settings.TARGET_USERNAME)
    filenames  = [settings.BIG_FILE]
    fout = os.path.join(settings.SRC_DIR_FILE, str(time.time()))
    
    with open(fout, "w") as fh_out:
    #    o = opener(cat(grep(pattern, writer(fh_out))))
        o = opener(cat(grep(pattern, writer())))
        o.send(settings.BIG_FILE)
    
    #print(RECSREAD,RECSMATCH)
    print(RECSMATCH)

if __name__ == "__main__":
    sys.exit(main())