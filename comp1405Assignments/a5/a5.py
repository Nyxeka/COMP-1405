"""
Assignment 5: sets and dictionaries
By Nicholas Hylands
"""

from random import randrange
import string
import time

#Oh the lovliness of decorators.
def print_timing(function):
    #this is a higher-order-function, which is meant to be ran
    #alongside/on top of other functions, to time how long
    #they take.
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = function(*args)
        t2 = time.time()
        #1000[.0] because we want to keep it as a floating point number
        print "---------------"
        print "    function: " + str(function.__name__) + "() took " + str((t2-t1)*1000.0) + " milliseconds"
        print "---------------"
        return result
    return wrapper

def big_list(n):
    """Create a list of n 'random' values in the range [-n/2,n/2]"""
    return [ randrange(-n//2, n//2) for i in range(n) ]


def get_words(f):
    """Extract a list of words from the file named f"""
    words = open(f).read().lower().split()
    words = [ string.translate(w, None, string.punctuation) for w in words ]
    return [ w for w in words if w != '']
    
varney = get_words("varney.txt")
words = set(get_words("words.txt"))

##############################################################################
# Question 1:

#put the @ operator before this, to tell the interpreter to call this function
#on top of whatever function is below it:
@print_timing
def unique(a):
    #takes a list, a, and changes it so that each of the values only appear once.
    b = set()
    results = []
    #if x is not in b, we add it to b.
    #then we add x to the results list.
    #so we might do this a million times, but that's okay because sets are fast.
    for x in a:
        if (x not in b):
            b.add(x)
            results += [x]
    return results

##############################################################################
# Question 2:
@print_timing
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

@print_timing
def only_once(a):
    #this function takes a list, a, and returns the elements in the list that
    #only appear once.
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
@print_timing
def spell_check(wordlist):
    global words
    bad_words = []
    for a in wordlist:
        if not a.lower() in words:
            bad_words += [a]
        
    return bad_words

##############################################################################
# Question 5:    
@print_timing
def anagrams(f):
    f_words = set(get_words(f))
    list_of_anagrams = dict()
    for i in f_words:
        key = "".join(sorted([c for c in i]))
        if key in list_of_anagrams:
            list_of_anagrams[key] += [i]
        else:
            list_of_anagrams[key] = [i]
    new = []
    for i,x in list_of_anagrams.items():
        if len(list_of_anagrams[i]) > 1:
            #new += ["'" + str(i) + "'" + ": " + ", ".join(x)]
            print "'" + i + "'" + ": " + ", ".join(x)
    #for i,x in new.items():c
    #    print x

##############################################################################
# Question 6:    
"""
I think the best way to do this would be to create a list for each of the 
different types of corrections.
"""

def changes_to_check(word):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    #single letter deletion:
    single_deletion = [word[:i] + word[i+1:] for i in range(len(word))]
    single_insertion = []
    for i in range(len(word)):
        for j in range(len(alphabet)):
            single_insertion += [word[:i] + alphabet[j] + word[i:]]
    single_changes = []
    for i in range(len(word)):
        for j in range(len(alphabet)):
            single_changes += [word[:i] + alphabet[j] + word[i+1:]]
    return set(single_deletion + single_insertion + single_changes)
    
@print_timing
def suggest_alternatives(w):
    #creates a set of possible changes to the word, then checks them against
    #a set of words that we know are words.'
    global words
    changes = changes_to_check(w)
    suggestions = []
    for i in changes:   
        if i in words:
            suggestions += [i]
    return suggestions


















