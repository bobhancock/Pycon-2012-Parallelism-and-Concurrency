import sys
#from cdecimal import *
from decimal import *
c = getcontext()
#c.prec = MAX_PREC

m = int(sys.argv[1])

#one = 1.
one = 1
s = 0


prev = [1]
print(prev)
for row in xrange(1, m):
    curr = [1]
    for index in xrange(1, row):
        s += 1
        curr.append(prev[index-1] + prev[index])
    curr.append(1)
    #print curr
    prev = curr


print s           