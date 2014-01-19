def countdown(n):
    while n > 0:
        yield n
        n -= 1
        
m = 10
x = countdown(m)
print(x)
for i in range(3):
    print("Countdown: {d}".format(d=x.next()))