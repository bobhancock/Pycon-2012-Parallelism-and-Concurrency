import sys
tracing = False

def trace(f):
    if tracing:
        def callf(*args, **kwargs):
            debug_log.write("Calling {fn}: {a}, {k}".format(fn=f.__name__,
                                                            a=args,
                                                            k=kwargs))
            r = f(*args, **kwargs)
            debug_log.write("{fn} returned {rc}".format(fn=f.__name__,
                                                        rc=r))
        return callf
    else:
        return f

def sq(f):
    def callf(*args, **kwargs):
        r = f(*args, **kwargs)
        return r*r
    return callf

@sq
def double(x):
    return x+x

@trace
def square(x):
    return x*x

if tracing:
    debug_log = open("debug.log", "w")

def main():
    r = double(2)
    print(r)


if __name__ == "__main__":
    sys.exit(main())
