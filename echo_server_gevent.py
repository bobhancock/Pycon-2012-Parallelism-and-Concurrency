from gevent.server import StreamServer
import time

# handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    #print ('New connection from %s:%s' % address)
    # makefile because we readline()
    fileobj = socket.makefile()
    
    while True:
        line = fileobj.readline()
        #print("read {l}".format(l=line))
        if not line:
            break
        if line.strip().lower() == 'quit':
            #print ("client quit "+str(time.time()))
            fileobj.write("ACK\n")
            fileobj.flush()
            break
        else:
            #request_num = line.split(":")[0]
            fileobj.write(line)
            fileobj.flush()
        #print ("echoed %r" % line)


if __name__ == '__main__':
    port = 2020
    server = StreamServer(('0.0.0.0', port), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print ('Starting echo server on port {p}'.format(p=port))
    server.serve_forever()
