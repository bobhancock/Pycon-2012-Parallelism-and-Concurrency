# Cycle through a list of URLs, open, and read the contents.
# args
#    howmany_proceses - how many worker processes to use
#    times_to_extend_url_list - how many times to cycle through the list of URLs
#    iterations - number of times to execute the loop
from concurrent import futures
import sys
import time
import settings
from util.increase import nextend
if int(sys.version_info.major) == 2:
    from urlclient.urlclient2 import load_url, load_url_mp
else:    
    from urlclient.urlclient import load_url, load_url_mp

sys.path.insert(0, settings.PACKAGE_PATH)
import dry.logger 

def main():
    usage="urlclient_futures t|p times_to_extend_url_list processes iterations"
    
    if len(sys.argv) < 5:
        print("Not enough arguments.  "+usage)
        return
    
    if sys.argv[1] .lower() == "t":
        process_type="threads"
    elif sys.argv[1].lower() == "p":
        process_type = "mp"
    else:
        print("Must specify t or p for thread or process as first argument.")
        print(usage)
        return
    
    times_to_extend_url_list = int(sys.argv[2])
    processes=int(sys.argv[3])
    iterations = int(sys.argv[4])
 
    urls = nextend(settings.URLS, times_to_extend_url_list)
    n = len(urls)
    timeout_secs=max(n*3, 60)
    logger = dry.logger.setup_log_size_rotating("log/urlclient_futures.log", 
                                                logname='urlclientfutures')
    
    logger.info("times_to_extend_url_list={i} processes={p} timeout={t} n={n} type={y}".format(i=times_to_extend_url_list, 
                                                                  p=processes,
                                                                  t=timeout_secs,
                                                                  n=n,
                                                                  y=process_type))
    elapsed_time = []
    for i in range(iterations):
        j = 0
        start = time.time()
        if process_type == "threads":
            with futures.ThreadPoolExecutor(max_workers=processes) as executor:
                future_to_url = dict( (executor.submit(load_url, url, logger, timeout_secs=30,logstatus=True), url) for url in urls )
        else:
            #urls=urls[:9]
            try:
                with futures.ProcessPoolExecutor(max_workers=processes) as executor:
                    future_to_url = dict( (executor.submit(load_url_mp, url, timeout_secs=10), url) for url in urls )
            except Exception as e:
                print(e)
                #logger.error(e)
                
        try:
            for future in futures.as_completed(future_to_url, timeout=timeout_secs):
                j += 1
                url = future_to_url[future]
        except Exception as e:
            #traceback.print_exc(file=sys.stdout)
            logger.error("j={j} url={u} e={e}".format(j=j, e=e, u=url))
            
        elapsed_time.append(time.time() - start)
            
    elapsed_time_str = ""
    for t in elapsed_time:
        elapsed_time_str += str(t)+","
    elapsed_time_str.strip,(",")
    
    print("{pt},{u},{np},{et}".format(pt=process_type, u=len(urls), np=processes,
                                      et=elapsed_time_str))
    
if __name__ == '__main__':
    main()