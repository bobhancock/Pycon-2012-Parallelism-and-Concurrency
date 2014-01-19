""" Demonstrate blocking IO from the command line. """

import os
text = ""
while True:
    if text.lower() == "quit":
        os.write(1, "He's dead, Jim!\n")
        break
    elif text:
        os.write(1, "You said, '{n}'\n".format(n=text))
        text = ""
    os.write(1, "->")
    while True:
        readval = os.read(0, 4)
        if readval[-1] == "\n":
            text += readval[:-1]
            break
        text += readval
                 