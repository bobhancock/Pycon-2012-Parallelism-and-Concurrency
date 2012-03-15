import os

PACKAGE_PATH="pypackages"
# File IO
MAX_FILES = 100

MAX_WRITES = 100000

MAX_ITERATIONS = 10

URLS = ("http://www.python.org",
    "http://dev.chromium.org/spdy",
    "http://mapreduce.stanford.edu",
    "http://www.ibm.com",
    "http://google.com",
    "http://www.bbc.co.uk/",
    "http://www.json.org/" ,
    "http://www.lemonde.fr/",
    "http://yahoo.com",
    "http://www.doughellmann.com/",
    "http://www.cnn.com",
    "http://www.nytimes.com",
    "http://www.bradmehldau.com",
    "http://bobhancock.org",
    "http://eventlet.net/doc/design_patterns.html",
    "http://golang.org/doc/effective_go.html",
    "http://blog.dynatrace.com/",
    "http://rss.cnn.com/rss/cnn_world.rss",
    "http://rss.cnn.com/rss/cnn_us.rss",
    "http://rss.cnn.com/rss/si_topstories.rss",
    "http://rss.cnn.com/rss/money_latest.rss",
    "http://rss.cnn.com/rss/cnn_allpolitics.rss", 
    "http://rss.cnn.com/rss/cnn_crime.rss",
    "http://rss.cnn.com/rss/cnn_tech.rss",
    "http://rss.cnn.com/rss/cnn_space.rss",
    "http://rss.cnn.com/rss/cnn_health.rss",
    "http://rss.cnn.com/rss/cnn_showbiz.rss",
    "http://rss.cnn.com/rss/cnn_travel.rss",
    "http://rss.cnn.com/rss/cnn_living.rss",
    "http://rss.cnn.com/rss/cnn_freevideo.rss",
    "http://rss.cnn.com/rss/cnn_mostpopular.rss",
    "http://rss.cnn.com/rss/cnn_latest.rss",
    "http://www.nytimes.com/services/xml/rss/nyt/Business.xml",
    "http://finance.yahoo.com/rss/headline?s=mhp",
    "http://www.ft.com/servicestools/newstracking/rss#world",
    "http://finance.yahoo.com/rss/headline?s=mhp",
    "http://golang.org",
    "http://www.weather.com",
    "http://ocw.mit.edu/courses/electrical-engineering-and-computer-science",
    "http://www.google.com/edu/computational-thinking/index.html")

TARGET_USERNAME = "ssbrtg"
SRC_DIR_FILE = "/home/rhancock"

# Specify the canonical path since this is also read by
# the Go programs.
#BIG_FILE = "xferlog/bigsmallfile.xferlog" #2 matches
BIG_FILE = "xferlog/bigmedfile.xferlog" # 12256 matches
#BIG_FILE = "xferlog/bigfile.xferlog" # 194,040 matches

# The number of chunks that file should be broken into.  One
# chunk for each thread or process.
BIGFILE_THREADS_CHUNKS=2
BIGFILE_MP_CHUNKS=3 #8 is sweet
BIGFILE_GEVENT_CHUNKS=4
BIGFILE_FUTURES_CHUNKS=4

# urlclient
URLCLIENT_THREADS=1
URLCLIENT_PROCESSES=18
URLCLIENT_ITERATIONS=5
