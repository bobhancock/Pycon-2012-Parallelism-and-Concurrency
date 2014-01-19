""" non-blocking io from command line """
import os, fcntl, time, errno

def nb_read(fd=None, length=None):
    readval = None
    while readval is None:
        try:
            readval = os.read(fd, length)
        except OSError, e:
            if e.errno != errno.EWOULDBLOCK:
                raise
            
        if readval is None:
            time.sleep(0.1)
            
    return readval
    
fhout = fcntl.fcntl(0, fcntl.F_GETFL)
fcntl.fcntl(0, fcntl.F_SETFL, fhout | os.O_NONBLOCK)

try:
    text = ""
    while True:
        if text.lower() == "quit":
            os.write(1, "Captain, Data has disappeared!\n")
            break
        elif text:
            os.write(1, "You said, '{n}'\n".format(n=text))
            text = ""

        os.write(1, "->")

        while True:
            readval = nb_read(fd=0, length=4)
            if readval[-1] == '\n':
                text += readval[:-1]
                break

            text += readval
finally:
    fcntl.fcntl(0, fcntl.F_SETFL, fhout)


