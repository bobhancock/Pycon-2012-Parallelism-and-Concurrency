# Build a list of n 
import time
import decimal
from random import random, randint

n = 100000000
l = [decimal.Decimal(random()) + decimal.Decimal(random()) for x in xrange(1, n)]


