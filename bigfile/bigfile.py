def chunk_end(fh, start):
    """
    From the end of the chunk, increment until you find a newline and
    return that position.
    """
    fh.seek(start)
    c = fh.read(1)
    while c != '\n' and c!= "": # empty string on EOF
        c = fh.read(1)
    return fh.tell()


def size_chunks(fh, fsize, num_chunks=4):
    """
    Create num_chunks equal chunks of the file.
    
    return
       A list of tuples (chunk_start, chunk_size)
    """
    chunks = []
    chunk_size = fsize / num_chunks
                
    start = 0
    for i in range(0, num_chunks):
        if (start + chunk_size < fsize):
            end = chunk_end(fh, start + chunk_size)
            size = (end - start)
        else:
            end = fsize
            size = (fsize - start)
            
        #print("i={i} chunk_end={e} chunk_start={s} chunk_size={z}".format(i=i,e=end,s=start,z=size))
        chunks.append((start, size))
        start = end + 1
    
    return chunks


def find(fh, chunk, pattern, q):
    """
    Seek to the start of a chunk and read each line.
    
    fh      File handle to the file
    chunk   A tuple (start, size of chunk)
    q       Synchronized queue
    """
    f = fh
    start, size = chunk
    recsmatch = 0
    
    bytes_read = 0
    f.seek(start)
    while bytes_read < size:
        line = f.readline()
        bytes_read += len(line)
        if pattern.search(line):
            recsmatch += 1

    q.put(recsmatch)

        
def count_matches(q):
    recsmatch = 0
    while True:
        matches = q.get()
        if matches == None: # sentinel
            q.task_done()
            break
        
        recsmatch += matches
        q.task_done()
        
    print(recsmatch)


def find_noq(fh, chunk, pattern):
    """
    Seek to the start of a chunk and read each line.
    This is used with programs that do not use a queue.
    
    fh      File handle to the file
    chunk   A tuple (start, size of chunk)
    q       Synchronized queue
    """
    f = fh
    start, size = chunk
    recsmatch = 0
    
    bytes_read = 0
    f.seek(start)
    while bytes_read < size:
        line = f.readline()
        bytes_read += len(line)
        #print(line)
        if pattern.search(line):
            recsmatch += 1

    return recsmatch

