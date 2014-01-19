# Test list comprehension
import time

n = 1000000000

s = time.time()
l = [i for i in range(n)]
print (time.time() - s)
    
