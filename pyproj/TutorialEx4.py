#Tutorial excersizes...
"""
a=1,j=2
a=1,j=3
...
a=1,j=n
a=2,j=n
etc...
"""

import random

def rand_array(n, x):
    result_array = []
    for i in range(n):
        result_array += random.randrange(-x, x+1)
    return result_array

def max_sum(a):
    #HA!
    list_of_possibilities = []
    for i in range(len(a)):
        for j in range(len(a)):
            if i < j:
                list_of_possibilities += [[i,j]]
    new_max = None
    new_result = []
    new_sum = 0
    old_sum = 0
    for i in range(len(list_of_possibilities)):
        new_sum = 0
        for j in range(list_of_possibilities[i][0],list_of_possibilities[i][1]):
            new_sum += a[j]
        if new_sum > old_sum:
            old_sum = new_sum
            new_result = list_of_possibilities[i]
        
    return new_result

    
#example input:
#'here we go again'
#'we gain'
#'green eggs and ham sandwhiches'
#'reggae'
#[5,6,12,13,14,15]
test_a = "we gain"
test_s = "here we go again"
def has_subsequence(a,s,cut=0):
    #after the first, we don't want fail for double letters...
    if len(s)==0:
        return []
    if len(a)==0:
        return []
    print a
    print s[cut:]
    for i in range(len(s[cut:])):
        if a[0] == s[cut+i]:
            return [cut+i] + has_subsequence(a[1:],s,cut+1+i)
        
def testit():
    return has_subsequence(test_a,test_s)