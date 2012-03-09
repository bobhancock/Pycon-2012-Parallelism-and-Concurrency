from greenlet import greenlet

def sub():
    print("sub is switching to two.")
    g2.switch()
    print("sub is done.")

    
def one():
    sub()
    
def two():
    print("two is switching to one.")
    g1.switch()
    print("two is done.")

    
    
g1 = greenlet(one)
g2 = greenlet(two)
print("main switching to one.")
g1.switch()
print("main is done.")