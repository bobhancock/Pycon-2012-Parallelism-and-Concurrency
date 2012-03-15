import gevent
from gevent import queue

q = queue.Queue()

for i in range(100000):
    q.put(i)
q.put(StopIteration)    

print q.qsize()