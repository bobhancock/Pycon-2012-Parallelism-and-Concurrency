import sys
#from cdecimal import *
#c = getcontext()
#c.prec = MAX_PREC

if len(sys.argv) < 2:
    print("usage: %prog iterations")
    sys.exit()

#m = 100000
m = int(sys.argv[1])
#one = 1
one = 1. 

prev = [one]
#print(prev)
for row in xrange(1, m):
    curr = [one]
    mid = (row /2)+1
        
    if row % 2 == 0:
        right = mid - 1
    else:
        right = mid
           
    for index in xrange(1, mid):
        curr.append(prev[index-1] + prev[index])
        
    r = curr[0:right]
    r.reverse()
    curr.extend(r)
    prev = curr
    #print(curr)

print(curr[mid])
