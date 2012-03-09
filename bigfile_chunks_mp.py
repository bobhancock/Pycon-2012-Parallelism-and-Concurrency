# Split the file into four chunks, process each chunk in a separate process,
# count the number of matching records, report via a queue, calculate total.
import os
import sys
import re
import time
import multiprocessing
from multiprocessing import JoinableQueue as Queue
import settings
from bigfile.bigfile import chunk_end, size_chunks, find, count_matches


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
con = multiprocessing.Process(target=count_matches, args=(q,))
con.daemon = True
con.start()

# producer
producers = []
file_handles = []

for chunk in chunks:    
    fh = open(sfile, "r")
    file_handles.append(fh)
    t = multiprocessing.Process(target=find, args=(fh, chunk, pattern, q))
    t.daemon = True
    producers.append(t)
    
for p in producers:
    p.start()

for p in producers:
    p.join()
    
q.put(None) # sentinel
con.join()

for f in file_handles:
    f.close()

print("chunks={c}".format(c=settings.BIGFILE_MP_CHUNKS))
