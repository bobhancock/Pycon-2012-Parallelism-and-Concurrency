from pprint import pprint
from collections import defaultdict

mylist = ['a',
 'b',
 'b/c',
 'b/d',
 'e',
 'f',
 'f/g',
 'f/h',
 'f/h/i',
 'f/h/i/j']

my_dict = lambda: defaultdict(my_dict)
d = my_dict()
for x in mylist:
    reduce(defaultdict.__getitem__, x.split("/"), d)
    
pprint(d)    