from functools import wraps

def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap    

#def memo(func):
    #cache = {}
    #@wraps(func)
    #def wrap(*args):
        #try:
            #return cache[args]
        #except KeyError:
            #ret = cache[args] = func(*args)
            #return ret
    #return wrap