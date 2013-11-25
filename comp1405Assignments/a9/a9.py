from __future__ import division

#Question 1:
def fib0(n):
    if n > 0:
        return 2**int(n)

#Question 2:
def fib3(n):
    a = [1]*n
    if n >= 3:
        for i in range(2, n):
            a[i] = a[i-1] + a[i-2] + a[i-3]
        return a[n-1]
    else:
        return 1

#Question 3:
def largest_two(a):
    b = a
    largest = max(b)
    b.remove(largest)
    second_largest = max(b)
    return largest + second_largest

#Question 4:
def smallest_half(a):
    number_of_values = len(a)/2
    a.sort()
    lowest_values = a[int(len(a)/2):]
    return sum(lowest_values)

#Question 5:
def median(a):
    b = a
    b.sort()
    half = int(len(a)/2)
    x = (b[half] + b[half+1])/2
    return x

#Question 6:
def majority(a):
    b = dict()
    
    for i in a:
        if i in b:
            b[i] += 1
        else:
            b[i] = 1
    values = list(b.values())
    keys = list(b.keys())
    biggest = keys[values.index(max(values))]
    if b[biggest] > (len(a)/2 + 1):
        return biggest
    else:
        return None

#Question 7:

def make_change(n,amounts):
    c = dict()
    
    for i in amounts:
        c[i] = 0
    
    x = float(n)/100
    
    for i in amounts:
        to_keep = x % i
        to_remove = x - to_keep
        
        c[i] += int(to_remove / i)
        x = to_keep
    return c
    

def canadian_change(n):
    rounded_cents = int(5 * round(float(n)/5))
    print "$%.2f is rounded to $%.2f" % (float(n)/100, float(rounded_cents)/100)
    amounts = [100,50,20,10,5,2,1,0.25,0.1,0.05]
    change = make_change(rounded_cents,amounts)
    if len(change) > 0:
        for i in amounts:
            if change[i] > 0:
                print str(change[i]) + " x $" + str(i)
                
#Question 8:
def triple_sum(a, x):
    result = []
    b = set(a)
    num_times = 0
    done = False
    for i in range(len(a)-1):
        for j in range(i+1, len(a)):
            number = x-(a[i]+a[j])
            num_times += 1
            if number in b:
                result.append(i)
                
                result.append(j)
                
                result.append(a.index(number))
                
                done = True
                break
        if done:
            break
    if result == []:
        result = None
    return result