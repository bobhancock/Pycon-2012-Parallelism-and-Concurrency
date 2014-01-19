# Multiprocessing won't work because the executor cannot serialize the object returned by 
# open(fname, "r").  Specifically, 
# <_io.TextIOWrapper name='/home/rhancock/bigsmallfile.xferlog' mode='r' encoding='UTF-8'>
from concurrent import futures
import sys
import os
import re
import time
import settings
from bigfile.bigfile import chunk_end, size_chunks, find_noq

sys.path.insert(0, settings.PACKAGE_PATH)
import dry.logger 

def main():
    start = time.time()
    logger = dry.logger.setup_log_size_rotating("log/bigfile_futures_threadpool.log", 
                                                logname='bigfilefuturesthreads')
    
    logger.info("START")
    elapsed_time = []
    
    sfile = settings.BIG_FILE
    fsize = os.path.getsize(sfile)
    with  open(sfile, "r") as fh:
        #A list of tuples (chunk_start, chunk_size)
        chunks = size_chunks(fh, fsize, num_chunks=settings.BIGFILE_FUTURES_CHUNKS)
    
    pattern = re.compile(settings.TARGET_USERNAME)
    file_handles = []
    for j in range(len(chunks)):
        file_handles.append(open(sfile, "r"))
    
    with futures.ThreadPoolExecutor(max_workers=settings.BIGFILE_FUTURES_CHUNKS) as executor:
        future_to_chunk = dict( (executor.submit(find_noq, file_handles[i], chunks[i], pattern), "") \
                                for i in range(len(chunks)) )
        
    recsmatch = 0    
    
    try:
        for future in futures.as_completed(future_to_chunk, timeout=60):
            recsmatch += future.result()
    except Exception as e:
        #traceback.print_exc(file=sys.stdout)
        logger.error("recsmatch={m} e={e}".format(m=recsmatch, e=e))
        return
            
    elapsed_time.append(time.time() - start)
            
    elapsed_time_str = ""
    for t in elapsed_time:
        elapsed_time_str += str(t)+","
    elapsed_time_str.strip,(",")
    
    print("{r}".format(r=recsmatch))
    logger.info("STOP|elapsedtime:{et}|recsmatch:{r}".format(et=elapsed_time, r=recsmatch))
    
if __name__ == "__main__":
    sys.exit(main())