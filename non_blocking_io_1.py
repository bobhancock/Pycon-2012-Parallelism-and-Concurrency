""" non-blocking io from the command line """
import os, fcntl, time

fhout = fcntl.fcntl(0, fcntl.F_GETFL)
fcntl.fcntl(0, fcntl.F_SETFL, fhout | os.O_NONBLOCK)
text = ""

while True:
    if text.lower() == "quit":
        os.write(1, "It just disappeared.\n"); break
    elif text:
        os.write(1, "You said, '{n}'\n".format(n=text))
        text = ""
    os.write(1, "->")
    time.sleep(5) # wait for user to input text

    while True:
        readval = os.read(0, 4)
        if readval[-1] == '\n':
            text += readval[:-1]
            break
        text += readval