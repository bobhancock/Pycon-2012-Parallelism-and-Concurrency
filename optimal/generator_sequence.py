# Test generaor sequence
# Only runs under python3 with this size.
# python2 produces a memory error.
import time
import sys
if sys.version_info.major != 3:
    print("This will only run under Python3.x")
    sys.exit(1)
    
def countdown(n):
    while n > 0:
        yield n
        n -= 1

n = 1000000000
s = time.time()
            
x = countdown(n)
for i in range(n):
    d = next(x)

print (time.time() - s)
    