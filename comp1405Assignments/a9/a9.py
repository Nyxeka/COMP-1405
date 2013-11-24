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
    largest = b.max()
    b.remove(largest)
    second_largest = b.max()
    return largest + second_largest

#Question 4:
def smallest_half(a):
    number_of_values = len(a)/2
    b = sort(a)
    c = b[(len(a)/2):]
    return sum(c)

#Question 5:
def median(a):
    b = sort(a)
    half = len(a)/2
    x = (b[half] + b[half+1])/2

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
    #the following was found here as the fastest method of grabbing the key of the biggest value in a fict
    #http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    biggest = keys[values.index(max(values))]
    if b[biggest] > (len(a)/2 + 1):
        return biggest
    else:
        return None

#Question 7:

def make_change(n,b=dict()):
    c = b
    
    if len(c) < 1:
        c[100] = 0
        c[50] = 0
        c[20] = 0
        c[10] = 0
        c[5] = 0
        c[2] = 0
        c[1] = 0
        c[0.25] = 0
        c[0.1] = 0
        c[0.05] = 0
        x = float(n)/10
    else:
        x = n
    if x > 0:
        if n >= 100:
            c[100] += 1
            x -= 100
        if x >= 50:
            c[50] += 1
            x -= 50
        if x >= 20:
            c[20] += 1
            x -= 20
        if x >= 10:
            c[10] += 1
            x -= 10
        if x >= 5:
            c[5] += 1
            x -= 5
        if x >= 2:
            c[2] += 1
            x -= 2
        if x >= 1:
            c[1] += 1
            x -= 1
        if x >= 0.25:
            c[0.25] += 1
            x -= 0.25
        if x >= 0.1:
            c[0.1] += 1
            x -= 0.1
        if x >= 0.05:
            c[0.05] += 1
            x -= 0.05
        return make_change(x,c)
    else:
        return c
    

def canadian_change(n):
    rounded_cents = int(5 * round(float(n)/5))
    print "$%.2f is rounded to $%.2f" % (float(n)/100, float(rounded_cents)/100)
    amounts = [100,50,20,10,5,2,1,0.25,0.1,0.05]
    change = make_change(rounded_cents)
    if len(change) > 0:
        for i in amounts:
            if c[i] > 0:
                print str(c[i]) + " x $" + str(i)
                
#Question 8:
def triple_sum(a, x):
    result = []
    b = set(a)
    done = False
    for i in range(len(a)-1):
        for j in range(i+1, len(a)):
            number = x-(a[i]+a[j])
            
            if number in b:
                result.append(i)
                
                result.append(j)
                
                result.append(a.index(number))
                
                done = True
                break
        if done:
            break
    return result
    
    