from greenlet import greenlet

def one():
    print("One is switching to two.")
    g2.switch()
    print("One is done.")
    
def two():
    print("Two is switching to one.")
    g1.switch()
    print("Two is done.")

    
g1 = greenlet(one)
g2 = greenlet(two)
print("main switching to one.")
g1.switch()
print("main is done.")