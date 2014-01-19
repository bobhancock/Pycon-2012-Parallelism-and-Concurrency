import time
r=0
start=time.time()
for i in xrange(316000000):
    r += 1
print(time.time() - start)
