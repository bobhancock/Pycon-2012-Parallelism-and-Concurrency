# Run it with and without memo to see the time difference.
from memo import memo
import sys

@memo
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def main():
    N = int(sys.argv[1])
    i = 1
    while i <= N:
        f = fib(i)
        i += 1
    print(f)
        
if __name__ == "__main__":
    main()
