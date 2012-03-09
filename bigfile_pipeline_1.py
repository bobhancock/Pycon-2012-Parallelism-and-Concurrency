""" Generator version of pipeline. """
#import os
import sys
import re
#import time
#import gzip
#import bz2

import settings

#RECSMATCH=0
#RECSREAD=0

def opener(filenames):
    """ Return a file handle to an open file. """
    for name in filenames:
        #if name.endswith(".gz"):
            #f = gzip.open(name)
        #elif name.endswith('.bz2'):
            #f = bz2.BZ2File(name)
        #else:
            #f = open(name)
            
        #yield f

        yield open(name)
        
        
def cat(filelist):
    """ Yield a line. """
    for f in filelist:
        for line in f:
            #RECSREAD += 1
            yield line 
            

def grep(lines, pattern):
    """ If the pattern is in the line, yield the line. """
    for line in lines:
        if pattern.search(line): #change to regex or re2
            yield line           
            
def starter(fnames):
    pattern = re.compile(settings.TARGET_USERNAME)
    filenames  = [settings.BIG_FILE]
        
    files = opener(filenames)
    lines = cat(files)
    xmit_lines = grep(lines, pattern)
    
    return xmit_lines
    
def main():
    #pattern = re.compile(settings.TARGET_USERNAME)
    #filenames  = [settings.BIG_FILE]
    ##fout = os.path.join(settings.SRC_DIR_FILE, str(time.time()))
    
    #files = opener(filenames)
    #lines = cat(files)
    #xmit_lines = grep(lines, pattern)
    
    #with open(fout, "w") as fh_out:
        #for line in xmit_lines:
            #fh_out.write(line)
  
    recsmatch = 0
    xmit_lines = starter([settings.BIG_FILE])
    for line in xmit_lines:
        recsmatch += 1
        
    #print(RECSREAD,RECSMATCH)
    print(recsmatch)
    
if __name__ == "__main__":
    sys.exit(main())    