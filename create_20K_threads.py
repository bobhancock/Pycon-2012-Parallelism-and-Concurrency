
from time import sleep
from threading import Thread
sleep_time = 10
n = 20000
threads = []
print("n=%d" % n)
for i in xrange(0, n):
    t = Thread(target=sleep, args=(sleep_time,))
    t.start()
    if i % 100 == 0:
        print(i)
    threads.append(t)
        
print("Sleeping a bit...")
sleep(60)
print("Threads created.  Now, joining...")

i = 0
for t in threads:
    t.join()
    i += 1
    if i % 100 == 0:
        print(i)

print("Done")
