import sys
import time
from coroutinedec import coroutine

@coroutine
def by_three():
    t = (yield)
    print("{n} is divisible by three".format(n=t))

@coroutine
def by_five():
    t = (yield)
    print("{n} is divisible by five".format(n=t))

@coroutine
def by_thirteen():
    t = (yield)
    print("{n} is divisible by thirteen".format(n=t))
    
    
def main():
    b3 = by_three()
    b5 = by_five()
    b13 = by_thirteen()
    
    while True:
        now = time.time()
        try:
            if now % 3 == 0:
                b3.send(now)
            if now % 5 == 0:
                b5.send(now)
            if now % 13 == 0:
                b13.send(now)
        except StopIteration:
            continue
            
        
if __name__ == "__main__":
    sys.exit(main())