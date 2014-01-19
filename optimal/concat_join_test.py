"""
Test join and concatenation.

Bob Hancock - hancock.robert@gmail.com
"""
import random
import time


def test_data_uniform(size):
    """ Create a list of random strings of relative uniform size. """
    chunks = []
    for i in range(size):
        chunks.append(str(random.random()))
        
    return chunks


def test_data_nonuniform(size):
    """ Create a list of random strings of increasing non-uniform size.
    Shuffle the result to insure that there is not a monotonic increase in size
    of elements."""
    chunks = []
    for i in range(size):
        c= ""
        for j in range(i):
            c += str(random.random())
        chunks.append(c)
        
    random.shuffle(chunks)
    return chunks


def join_chunks(chunks, join_time):
    start = time.time()
    r = "".join(chunks)
    join_time.append(time.time() - start)
    
    
def concat_chunks(chunks, concat_time): 
    r = ""
    start = time.time()
    for c in chunks:
        r += c
    concat_time.append(time.time() - start)
    
    
def fmt_times(times):
    return "total time: {total} min: {min} max: {max} mean: {mean}".format(total=sum(times),min=min(times), max=max(times), mean=sum(times)/len(times))

    
def testit(n, uniform=True):
    concat_time = []
    join_time = []

    # Create lists of size n
    if uniform:
        chunks = test_data_uniform(n)
    else:
        chunks = test_data_nonuniform(n)

    # Concat and join each list n times and record the time for each.
    for i in range(n):
        join_chunks(chunks, join_time)
        concat_chunks(chunks, concat_time)
    
    u = "uniform" if uniform else "non-uniform"
    
    print("{u} size data n={n}".format(u=u, n=n))
    print("-"*40)
    print("join - "+fmt_times(join_time))
    print("concat - "+fmt_times(concat_time))
    print("")


# Start here
testit(50)
testit(50,False)
#testit(500)
testit(5000)
testit(500, False)
#testit(5000, False)  // you need a lot of memory!
