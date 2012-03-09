"""
0 = record type for read start (so it sorts correctly).
1 = record type for read complete.
"""
import urllib2
import time
import uuid

def load_url(url, logger, timeout_secs=20, logstatus=False):
    start = time.time()
    uid = uuid.uuid4()
    
    if logstatus:
        logger.info("{i}|{u}|0|{t}".format(u=url,i=uid, t=timeout_secs))

    try:
        data = urllib2.urlopen(url, timeout=timeout_secs).read()
    except Exception as e:
        logger.error("{i}|{u}|2|{t}|{et}|{e}".format(u=url,
                                                     i=uid,
                                                     t=timeout_secs,
                                                     et=time.time() - start,
                                                     e=e))

    if logstatus:
        logger.info("{i}|{u}|1|{et}".format(i=uid, u=url, et=time.time() - start))


def load_url_mp(url, timeout_secs=20):
    """
    multiprocessing cannot serialize a logger instance.
    """
    start = time.time()
    uid = uuid.uuid4()

    try:
        data = urllib2.urlopen(url, timeout=timeout_secs).read()
    except Exception as e:
        print("{i}|{u}|2|{t}|{et}|{e}".format(u=url,
                                              i=uid,
                                              t=timeout_secs,
                                              et=time.time() - start,
                                              e=e))          


    msg =  "{u},opGet,{t}".format(u=url,l=len(data),t=time.time()-start)
    return msg          