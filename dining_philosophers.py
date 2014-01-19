import threading
import random
import time
 
# Dining philosophers, 5 Philosphers with 5 chopsticks. 
# Must have two chopstick to eat.
# Deadlock is avoided by never waiting for a chopstick while holding a chopstick (locked)
#  
# dining philosophers http://en.wikipedia.org/wiki/Dining_philosophers_problem
# 'live lock' http://en.wikipedia.org/wiki/Livelock#Livelock
 
class Philosopher(threading.Thread):
 
    running = True
 
    def __init__(self, xname, chopstickOnLeft, chopstickOnRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.chopstickOnLeft = chopstickOnLeft
        self.chopstickOnRight = chopstickOnRight
 
    def run(self):
        while(self.running):
            #  Philosopher is thinking (but really is sleeping).
            time.sleep( random.uniform(3,13))
            print("{n} is hungry.".format(n=self.name))
            self.dine()
 
    def dine(self):
        chopstick1, chopstick2 = self.chopstickOnLeft, self.chopstickOnRight
 
        while self.running:
            chopstick1.acquire(True)
            locked = chopstick2.acquire(False)
            if locked: break
            chopstick1.release()
            print("{n} swaps chopstick".format(n=self.name))
            chopstick1, chopstick2 = chopstick2, chopstick1
        else:
            return
 
        self.dining()
        chopstick2.release()
        chopstick1.release()
 
    def dining(self):			
        print("{n} starts eating".format(n=self.name))
        time.sleep(random.uniform(1,10))
        print("{n} finishes eating and starts to think.".format(n=self.name))
 
def DiningPhilosophers():
    chopstick = [threading.Lock() for n in range(5)]
    philosopher_names = ('Aristotle','Kant','Buddha','Marx', 'Russell')
 
    philosophers= [Philosopher(philosopher_names[i], chopstick[i%5], chopstick[(i+1)%5]) \
            for i in range(5)]
 
    random.seed(507129)
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(100)
    Philosopher.running = False
    print("Now we're finishing.")
 
DiningPhilosophers()