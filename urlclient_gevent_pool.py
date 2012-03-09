import sys
import time
import random
from statlib import stats
from util.increase import nextend
import settings

import gevent
from gevent.pool import Pool

from gevent import monkey
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()
from gevent import queue
from urlclient.urlclient2 import load_url

sys.path.insert(0, settings.PACKAGE_PATH)
import dry.logger 

qtimes = queue.Queue()
qerr = queue.Queue()
qstart = queue.Queue()


def main():
    #global qtimes,qerr
    usage="urlclient_futures times_to_extend_url_list processes iterations"
    if len(sys.argv) < 4:
        print("Not enough arguments.  "+usage)
        return        

    times_to_extend_url_list = int(sys.argv[1])
    processes=int(sys.argv[2])
    iterations=int(sys.argv[3])

    urls = nextend(settings.URLS, times_to_extend_url_list)
    random.shuffle(urls)
    n = len(urls)
    timeout_secs=max(n/10, 60)

    logger = dry.logger.setup_log_size_rotating("log/urlclient_gevent_pool.log", 
                                                logname="urlclientgeventpool")

    logger.info("START|times_to_extend_url_list:{i}|processes:{p}|timeout:{t}|urls:{n}|type:gevent".format(i=times_to_extend_url_list, 
                                                                                                           p=processes,
                                                                                                           t=timeout_secs,
                                                                                                           n=n))

    pool = Pool(max(processes, 4))
    qurltime = queue.Queue()
    elapsed_time = []
    for i in range(iterations):
        start = time.time()
        try:
            jobs = [pool.spawn(load_url, url, logger, timeout=60, logstatus=True) for url in urls]
            pool.join(timeout=timeout_secs)
        except Exception as e:
            logger.error(e)

        elapsed_time.append(time.time() - start)

    elapsed_time_str = ""
    for t in elapsed_time:
        elapsed_time_str += str(t)+","
    elapsed_time_str.strip,(",")

    print("g,{u},{np},{et}".format(u=len(urls), np=processes, et=elapsed_time_str))


        #if not qerr.empty():
            #qerr.put(StopIteration)
            #for err in qerr:
                #print(err)

        #print("jobs size {s}".format(s=len(jobs)))
        #print("qstart size {n}".format(n=qstart.qsize()))
        #print("qtimes size {n}".format(n=qtimes.qsize()))
        #qtimes.put(StopIteration)
        #times = []
        #for item in qtimes:
            #times.append(item)

        #print("Min {t}".format(t=min(times)))
        #print("Max {t}".format(t=max(times)))
        #print("Mean {t}".format(t=stats.mean(times)))
        #print("StdDev {t}".format(t=stats.stdev(times)))
        # This could block forever
        # How to handle queues?
        #for item in qurltime:
            #logger.info(item)

if __name__ == "__main__":
    sys.exit(main())