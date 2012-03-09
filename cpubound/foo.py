class Foo():
    clvar = 6
    
    def __init__(self):
        self.i = 9
        
    @classmethod
    def classm(cl):
        print("classm")
        
    @staticmethod
    def staticm():
        print("staticm")
        
    def bar(self):
        print("bar")
        
    
Foo.staticm()        
Foo.classm()
f = Foo()
f.bar()
fb = f.bar
fb()
print(f.i)
print(Foo.clvar)