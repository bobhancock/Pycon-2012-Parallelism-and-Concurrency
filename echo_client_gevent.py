"""
Create a thundering heard.
1.   Open 20,000 connections.
2.   Send 1024 packet_size packets n times from each connection.
"""

import socket 
import time
import sys
import gevent
import gevent.queue
#import ptime
from statlib import stats

port = 2020 
packet_size = 1024
msg = "Z" * packet_size +"\n"

qtimes = gevent.queue.Queue()
#qstart = gevent.queue.Queue()
#qerrors = gevent.queue.Queue()

#cons_quit = 0
invalid_responses = 0

def echo(c):
    global msg, invalid_responses#, qtimes, qstart, cons_quit

    for i in range(reps):
        t = time.time()
        #qstart.put(t)
        try:
            c.sendall(msg)
        except Exception as e:
            print(e)
            continue
        #qerrors.put(e)

        received_data = False
        remaining = packet_size + 1

        while (not received_data):
            data = ''
            chunk_parts = []
            chunk = ''
                
            while remaining > 0:
                chunk = ''
                chunk = c.recv(packet_size + 1)
                if len(chunk) == 0 and remaining > 0:
                    break
                    
                chunk_parts.append(chunk)
                remaining -= len(chunk)
                    
            # The join is about 18x faster than concatenation
            data = b"".join(chunk_parts)
            received_data = True
            #if len(data) != len(msg):
            if data != msg:
                print("len received_data={r}  len msg={m}".format(r=len(data),
                                                                  m=len(msg)))
                print(data)
            else:
                qtimes.put(time.time() - t)
    c.send("quit\n")
    data = c.recv(packet_size)
    c.close()

    #cons_quit += 1
    #if (cons_quit % 100) == 0:
    #    print cons_quit
    #print("Echo complete {t}".format(t=time.time()))


# Start execution
usage="echo_client_gevent.py host max_connections iterations"

if len(sys.argv) < 4:
    print(usage)
    sys.exit(1)
    
host = sys.argv[1]    
max_connections = int(sys.argv[2])
reps = int(sys.argv[3])

connections = []
for i in range(max_connections):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.connect((host,port)) 
    connections.append((sock,i))
    #print("Opened {n}".format(n=i))

jobs = [gevent.spawn(echo, sock) for sock,j in connections]
timeout_secs = len(jobs*2)
gevent.joinall(jobs, timeout=timeout_secs, raise_error=True) 
time.sleep(1.0)

#print("Closing conns")
#time.sleep(1.0)
#for c, j in connections:
    #print("Closing conn {i}".format(i=j))
    #c.close()

#print("Checking for errors")
#if qerrors.qsize():
    #for err in qerrors:
        #print(err)
        
 #if qstart.qsize():
    #print("START: {e}".format(e=qstart.qsize()))
        
print("Build times")
bstart = time.time()
times = []    
#i =0
if qtimes.qsize():
    qtimes.put(StopIteration)
    #print(qtimes.qsize())
    for item in qtimes:
        #i += 1
        #print(i, item)
        times.append(item)
        
# The len of times[] indicates the number or successful responses.
# The len should equal max_connections * iterations from the command line.
print("Time spent building time[]: {t} len={l}".format(t=time.time() - bstart, l=len(times)))
print("Round trip time:")
print("Min {t}".format(t=min(times)))
print("Max {t}".format(t=max(times)))
if sys.version[0] == "2":
    print("Mean {t}".format(t=stats.mean(times)))
    print("StdDev {t}".format(t=stats.stdev(times)))
#print("Invalid responses={i}".format(i=invalid_responses))
      
