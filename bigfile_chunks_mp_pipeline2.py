# Hangs after about 11 million records

import os
import sys
import re
import time
import multiprocessing
from multiprocessing.queues import SimpleQueue as Queue
import settings
from bigfile.bigfile import chunk_end, size_chunks, find, count_matches
from bigfile_pipeline_2 import opener, grep#, writer
from coroutinedec import coroutine


RECSMATCH = 0


@coroutine        
def cat(chunk, target_coroutine):
    """How to get cat to read only to the end of the chunk"""
    start, size = chunk
    bytes_read = 0
    keepgoing=True
    while True:
        f = (yield)
        f.seek(start)
        
        while bytes_read < size:
            line = f.readline()
            print(line.split(" ")[0])
            bytes_read += len(line)
            target_coroutine.send(line)


@coroutine            
def writer(q):
    global RECSMATCH
    while True:
        line = (yield)
        print("Match")
        q.put(1)

        
def sender(o):
    """ Kicks off the pipeline. """
    print("sender started")
    o.send(settings.BIG_FILE)
     
def main():
    sfile = settings.BIG_FILE
    fsize = os.path.getsize(sfile)
    with  open(sfile, "r") as fh:
        chunks = size_chunks(fh, fsize, num_chunks=settings.BIGFILE_MP_CHUNKS)
    
    # Debug
    #for c in chunks:
        #print(c)
        
    q = Queue()
    pattern = re.compile(settings.TARGET_USERNAME)
    
    # consumer
    #con = multiprocessing.Process(target=opener, args=(cat(grep(pattern, writer())),))
    #con.daemon = True
    #con.start()
    
    # producer
    producers = []
    file_handles = []
    for chunk in chunks:    
        fh = open(sfile, "r")
        file_handles.append(fh)
        o = opener(cat(chunk, grep(pattern, writer(q))))
        t = multiprocessing.Process(target=sender, args=(o,))
        t.daemon = True
        producers.append(t)
        
    for p in producers:
        p.start()
        
    
    for p in producers:
        p.join()
        
    #con.join()
    q.put(None) # sentinel
    
    for f in file_handles:
        f.close()
        
    recsmatch = 0 
    print("Before queue comp")
    while True:
        x = q.get()
        if x == None:
            break
        recsmatch += 1
    print("After queue comp")
        
    
    print("recsmatch={r} chunks={c}".format(r=recsmatch,
                                        c=settings.BIGFILE_MP_CHUNKS))

if __name__ == "__main__":
    sys.exit(main())