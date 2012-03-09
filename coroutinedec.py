""" Prinme a coroutine. """
def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        #cr.next()
        return cr
    return start