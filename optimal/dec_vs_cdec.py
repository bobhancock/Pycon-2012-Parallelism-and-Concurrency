import sys
import decimal 
import cdecimal
from random import random, randint
import time
  
usage = "usage: dec_vs_cdec.py datasize"
if len(sys.argv) < 2:
    print(usage)
    sys.exit()

m = int(sys.argv[1])
print("Data size is %d\n" % m)
print("decimal: {c}\n".format(c=decimal.getcontext()))
print("cdecimal: {c}\n".format(c=cdecimal.getcontext()))
print "-"*80

s = 0
start = time.time()
for x in xrange(1, m):
    s += randint(1,m)
print("integer: elapsed time={t} sum={s}".format(t=time.time() - start, s=s))
print "-"*80

s = 0
start = time.time()
for x in xrange(1, m):
    s += random()
print("float: elapsed time={t} sum={s}".format(t=time.time() - start, s=s))
print "-"*80

s = 0
start = time.time()
for x in xrange(1, m):
    s += decimal.Decimal(random()) 
print("decimal: elapsed time={t} sum={s}".format(t=time.time() - start, s=s))
print "-"*80

s = 0    
start = time.time()
for x in xrange(1, m):
    s += cdecimal.Decimal(random()) 
print("cdecimal: elapsed time={t} sum={s}".format(t=time.time() - start, s=s))
print "-"*80


