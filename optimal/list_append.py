# Test append items
import time

n = 1000000000
lst = []

start = time.time()
for i in range(n):
    lst.append(1)
print("append: n={n} elapsed seconds= {e}".format(n=n, e=time.time() - start))    
