# Split the file into four chunks and assign each to a thread.
# We don't calculate the records read because this would require
# synchronizing the value with locks or creating a separate queue.
# This would add an overhead that would skew the results when compared
# to the brute force approach.
import os
import sys
import re
import time
import threading
v = sys.version

if v[0] == "3":
    from queue import Queue
else:    
    from Queue import Queue

import settings
from bigfile.bigfile import size_chunks, chunk_end, find, count_matches

# Start Execution
if len(sys.argv) < 1:
    print("usage: bigfile_chunks")
    sys.exit(1)
    
sfile = settings.BIG_FILE
fsize = os.path.getsize(sfile)
        
with open(sfile, "r") as fh:
    chunks = size_chunks(fh, fsize, num_chunks=settings.BIGFILE_THREADS_CHUNKS)

q = Queue()
pattern = re.compile(settings.TARGET_USERNAME)

# consumer
# Use write_lines if you want an report of matches
#con = threading.Thread(target=write_lines, args=(q, fh_out))
con = threading.Thread(target=count_matches, args=(q,))
con.daemon = True
con.start()

# producer
producers = []
file_handles = []
for chunk in chunks:    
    fh = open(sfile, "r")
    file_handles.append(fh)
    t = threading.Thread(target=find, args=(fh, chunk, pattern, q))
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
    
print("chunks={c}".format(c=settings.BIGFILE_THREADS_CHUNKS))  
    