""" Python 3 """
import time
import uuid
import urllib.request

def load_url(url, logger, timeout_secs=20, logstatus=False):
    start = time.time()
    uid = uuid.uuid4()
    if logstatus:
        logger.info("{i}|{u}|0|{t}".format(u=url,i=uid, t=timeout_secs))

    try:
        b = urllib.request.urlopen(url, timeout=timeout_secs).read()
    except Exception as e:
        logger.error("{i}|{u}|2|{t}|{et}|{e}".format(u=url,
                                                     i=uid,
                                                     t=timeout_secs,
                                                     et=time.time() - start,
                                                     e=e))          

    if logstatus:
        logger.info("{i}|{u}|1|{et}".format(i=uid, u=url, et=time.time() - start))    

    return "{u},opGet,{t}".format(u=url,l=len(b),t=time.time()-start)


def load_url_mp(url, timeout_secs=20):
    """
    multiprocessing cannot serialize a logger instance.
    """
    start = time.time()
    uid = uuid.uuid4()

    try:
        b = urllib.request.urlopen(url, timeout=timeout_secs).read()
    except Exception as e:
        print("{i}|{u}|2|{t}|{et}|{e}".format(u=url,
                                              i=uid,
                                              t=timeout_secs,
                                              et=time.time() - start,
                                              e=e))          

    msg =  "{u},opGet,{t}".format(u=url,l=len(b),t=time.time()-start)
    print(msg)
    return msg