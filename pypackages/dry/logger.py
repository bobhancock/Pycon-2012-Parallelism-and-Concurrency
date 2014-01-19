"""
	Loging utilities.

	Sirguey-Hancock, Ltd.
"""
import logging
import logging.handlers
import threading
import time

def setupLogging(fLog, name='thislog', debug = False):
    """ Setup standard file logging """
    filenameLog = fLog
    isDebug = debug
    logname = name

    try:
        log = logging.getLogger(logname)
        if isDebug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s:%(levelname)s:%(message)s',
                                filename=filenameLog,
                                filemode='a')
        else:			
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s:%(levelname)s:%(message)s',
                                filename=filenameLog,
                                filemode='a')
    except Exception as e:
        raise e

    return log

def setup_log_timed_rotating(log_filename, 
                             logname='defaultlog',
                             rotate_when='midnight',
                             interval_time=60,
                             debug=False, 
                             backups = 32):
    """ Calculate the real rollover interval, which is just the number of
    # seconds between rollovers.  Also set the filename suffix used when
    # a rollover occurs.  Current 'when' events supported:
    # S - Seconds
    # M - Minutes
    # H - Hours
    # D - Days
    # midnight - roll over at midnight
    # W{0-6} - roll over on a certain day; 0 - Monday
    #
    # Case of the 'when' specifier is not important; lower or upper case
    # will work.    
    """
    when_to_rotate = rotate_when
    intval = interval_time
    name = logname
    isdebug = debug
    backup_count = backups
    log_file = log_filename
    
    log = logging.getLogger(name)
    
    lh = logging.handlers.TimedRotatingFileHandler(log_file,
                                                   when=when_to_rotate, 
                                                   interval=intval,
                                                   backupCount=backup_count,
                                                   encoding='utf-8')
    if isdebug:
        log.setLevel(logging.DEBUG)
        lh.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
        lh.setLevel(logging.INFO)
        
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    lh.setFormatter(formatter)
    log.addHandler(lh)
    
    return log

def setup_log_size_rotating(log_filename, 
                             logname='defaultlog',
                             max_size_in_bytes=(1024 * 1000000), 
                             debug=False, 
                             backups = 32):
    """ The file will rollover when it approaches maxBytes.
    Our default size is 1MB
    """
    max_bytes = max_size_in_bytes
    name = logname
    isdebug = debug
    backup_count = backups
    log_file = log_filename
    
    log = logging.getLogger(name)
    
    lh = logging.handlers.RotatingFileHandler(log_file,
                                              maxBytes=max_bytes, 
                                              backupCount=backup_count,
                                              encoding='utf-8')
    
    if isdebug:
        log.setLevel(logging.DEBUG)
        lh.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
        lh.setLevel(logging.INFO)
        
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    lh.setFormatter(formatter)
    log.addHandler(lh)
    
    return log

class Heartbeat(threading.Thread):
    """ Write string 'heartbeat' to log every n seconds, where 
    n = inter_rsync_time / 2.
    """
    def __init__(self, appconf, logger):
        # appconf is a dictionary with configuration values
        threading.Thread.__init__(self)
        self.appconf = appconf
        self.log = logger
        self.Kill = False

    def run(self):
        self.log.info('Entered Heartbeat.run()')
        basetime = int(0)
        inter_rsync_time = self.appconf['inter_rsync_time']
        inter_heartbeat_time = int(inter_rsync_time / 2 )

        try:
            while (not self.Kill):
                if (time.time() > basetime + inter_heartbeat_time):
                    self.log.info('heartbeat')
                    basetime = time.time()
                else:
                    time.sleep(float(1))
        except Exception as e:
            raise e

    def killMe(self):
        self.Kill = True
        self.log.debug('Heartbeat:self.Kill = True')
        