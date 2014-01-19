from coroutinedec import coroutine

@coroutine
def echo_emphasis():
    while True:
        s = (yield)
        print("{s}!".format(s=s))
              
e = echo_emphasis()
e.send("Hello, world")
e.send("I am leaving now")

