# Split the file into four chunks and assign each to a thread.
# We don't calculate the records read because this would require
# synchronizing the value with locks or creating a separate queue.
# This would add an overhead that would skew the results when compared
# to the brute force approach.
import os
import sys
import re
import time
import gevent
import gevent.queue

if sys.version[0] == "3":
    from queue import Queue
else:    
    from Queue import Queue

import settings
from bigfile.bigfile import chunk_end, size_chunks, find
        
def count_matches(q):
    recsmatch = 0
    while True:
        matches = q.get()
        if matches == None: # sentinel
            break
        
        recsmatch += matches

    print(recsmatch)
        
# Start Execution
if len(sys.argv) < 1:
    print("usage: %prog")
    sys.exit(1)
    
sfile = settings.BIG_FILE

fsize = os.path.getsize(sfile)
with open(sfile, "r") as fh:
    chunks = size_chunks(fh, fsize, num_chunks=settings.BIGFILE_GEVENT_CHUNKS)

pattern = re.compile(settings.TARGET_USERNAME)

# maxsize = 0 makes the queue act like a channel.  The queue will block
# until a get call retrieves the data.  In effect, it works like a CSP.
q = gevent.queue.Queue(maxsize=0)

# consumer
con = gevent.spawn(count_matches, q)

# producer
fhandles = [open(sfile, "r") for i in xrange(0, settings.BIGFILE_GEVENT_CHUNKS)]
jobs = [gevent.spawn(find, fhandles[i], chunks[i], pattern, q) for i in xrange(0, settings.BIGFILE_GEVENT_CHUNKS)]
gevent.joinall(jobs, timeout=10)

#q.put(None)
#con.join()

for f in fhandles:
    f.close()
    
#print("chunks={c}".format(c=settings.BIGFILE_GEVENT_CHUNKS))
