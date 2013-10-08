"""
Assignment 5: sets and dictionaries
By Nicholas Hylands
"""

from random import randrange
import string

def big_list(n):
    """Create a list of n 'random' values in the range [-n/2,n/2]"""
    return [ randrange(-n//2, n//2) for i in range(n) ]


def get_words(f):
    """Extract a list of words from the file named f"""
    words = open(f).read().lower().split()
    words = [ string.translate(w, None, string.punctuation) for w in words ]
    return [ w for w in words if w != '']

##############################################################################
# Question 1:    slept in after turning alarm off on a test day
>fullpanicmode.jpg
Thankfully test isn't for another 6 hours but still...

def unique(a):
    b = set(a)
    return b

##############################################################################
# Question 2:    

def negated(a):
    #since sets will remove duplicates, using sets for this question is absolutely pointless.
    #Also assumed that this is given an integer...
    b = set(a)
    c = []
    for i in b:
        if -i in b:
            c += [i]
    return c

##############################################################################
# Question 3:    


def only_once(a):
    freq = dict()
    c=[]
    for w in a:
        freq[w] = 0
    for w in a:
        freq[w] += 1
    for i, w in freq.items():
        if w == 1:
            c += [i]
    return c

##############################################################################
# Question 4:    

