from greenlet import greenlet

def test1():
    print("test1 is switching to g2")
    g2.switch()
    print("test1 done")
    
def test2():
    print("test2 switching to g1")
    g1.switch()
    print("test2 done")
    
g1 = greenlet(test1)
g2 = greenlet(test2)
print("main switching to g1")
g1.switch()
print("main done")
    