import sys

def fib(n):
    a, b = 0, 1
    i = 0
    while i <= n:
        #print(a)
        i += 1
        a, b = b, a+b

n = int(sys.argv[1])
i = 0
fib(n)