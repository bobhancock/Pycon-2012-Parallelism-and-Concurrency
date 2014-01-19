import sys
import urllib2
import gevent
from gevent import monkey
monkey.patch_all()

from util.increase import nextend
from urlclient.urlclient2 import load_url
import settings
sys.path.insert(0, settings.PACKAGE_PATH)
import dry.logger 

urls = settings.URLS

#def print_head(url, timeout_secs, logger):
    ##print ('Starting %s' % url)
    #try:
        #data = urllib2.urlopen(url, timeout=timeout_secs).read()
    #except Exception as e:
        #logger.error("{u} exception: {e}".format(u=url, e=e))
          
def main():
    usage="urlclient_futures iterations"
    if len(sys.argv) < 2:
        print(usage)
        return
        
    iterations = int(sys.argv[1])
    urls = nextend(settings.URLS, iterations)
    n = len(urls)
    timeout_secs=max(n/4, 60)
    
    logger = dry.logger.setup_log_size_rotating("log/urlclient_gevent_individual.log", 
                                                logname='urlclientgeventindividual')
    
    logger.info("iterations={i} timeout={t} n={n} type=gevent".format(i=iterations, 
                                                                  t=timeout_secs,
                                                                  n=n))
    
    jobs = [gevent.spawn(load_url, url, logger, timeout=60, 
                         logstatus=True) for url in urls]
    gevent.joinall(jobs, timeout=timeout_secs)  
    
if __name__ == "__main__":
    sys.exit(main())    

