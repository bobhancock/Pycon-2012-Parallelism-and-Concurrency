# Extend an list n times
import time
chunk = [1] 
n = 1000000000
lst = [1]

start = time.time()
for i in xrange(n):
    lst.extend(chunk)
print("extend: n={n} elapsed seconds={e}".format(n=n,e=time.time() - start))    