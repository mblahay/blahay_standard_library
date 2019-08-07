# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 09:57:12 2018

@author: mb18433
"""
import math
import itertools
from functools import reduce
from collections import defaultdict

def nvl(value,alternate_value): # Similar concept to NVL function available in Oracle databases
    """Provides for in-line substition of a None value.

    If "value" is not None, then it will be returned; otherwise, if "value"
    is None, then the "alternate_value" will be returned.

    Both the value to be tested and an alternate value must be passed in.

    This function mimics the functionality of the NVL function available
    in Oracle databases.
    """
    if value == None:
        return alternate_value
    return value
    
def zil(arg,alt_val=None): #zil stands for "zero item list," though the method works with anything that you can use len() with
    'Allows for the substitution of value if passed in argument has a length of zero'
    if len(arg) == 0:
        return alt_val
    return arg
    
def select(fields, record):
    '''Returns a version of the dict record with only the designated fields. 
       If field does not exist in source record, then in the new recordd the 
       dict key is assigned a value of None'''
    return {x:record.get(x) for x in fields}

def anyin(l1,l2):
    # return any([ x in l2 for x in l1]) #Could use this, but decided to write logic to short circuit the process
    for i in l1:
        if i in l2:
            return True        
    return False        

def nfunc(arg, function = None, alt_function = None, alt_val = None):
    '''
    Similar in concept to nvl, but used with function calls. The need for this 
    method arrises out of python's weak typing model because it is possible to 
    receive different types back from function calls. As such it is sometimes
    difficult to manage calling return objects functions as the desired method
    may not alwasy be available. This method allows you to define an alternate
    execution path based on the non-existance of the desired method.
    '''
    if arg:
        if function:
            return function(arg)
        else:
            return arg
    else:
        if alt_function:
            return alt_function(alt_arg)
        else:
            return alt_val
        
def isprime(arg):
    if type(arg) != int:
        raise TypeError('Value for prime checking must be of type int')
    if arg < 1:
        raise ValueError('Value for prime checking must be positive integer')
    if arg not in [1,2]: # One and Two are special cases that don't test right with the below for loop
        for i in itertools.chain(range(2,3),range(3,math.floor(math.sqrt(arg)) + 1,2)): # Only need to check from 2 up to the square root of the number being checked.
            if arg%i == 0:
                return False
    return True
    
def primes(begin=1,end=-1):
    'A generator for prime numbers.Will iterate through a given range and return all prime numbers'
    if end == -1:
        end = begin + 1000 - 1
    if begin % 2 == 0 and begin != 2: 
        begin = begin + 1
    if end % 2 == 0: 
        end = end - 1
    for i in range(begin,end+1,2):
        if isprime(i): yield i
        
def nested_loops_join(left=[],right=[],left_key=lambda x:x,right_key=lambda x:x,comparitor=lambda o,i:o==i, left_outer_join=False):
    'Generator that performs nested loops join upon two iterables.'
    for o in left:
        matched=False
        for i in right:
            if comparitor(left_key(o),right_key(i)):
                matched=True
                yield (o,i)
        if left_outer_join and not matched:
            yield(o,None)

def merge_join(left=[],right=[],left_key=lambda x:x,right_key=lambda x:x):
    'Generator that performs a merge join upon two iterables. Iterables must be sorted'
    
    # Right now this will only work on sorted and unique sets of data. Work needs to be done
    # to add the functionality that allows for this to work on non-unique sets

    # This is a helper function that retieves the next value and whether the iterator is exhausted.    
    def getnext(i):
        try:
            return (next(i), False)
        except StopIteration:
            return (None, True)

    # Setting up initial values 
    left_iter, right_iter = iter(left), iter(right)
    left_val,left_exhausted = getnext(left_iter)
    right_val,right_exhausted = getnext(right_iter)
   
    while not left_exhausted and not right_exhausted:
        if left_key(left_val) == right_key(right_val):
            yield (left_val,right_val)
        if not right_exhausted and left_key(left_val) > right_key(right_val):
            right_val,right_exhausted = getnext(right_iter)
        else:
            left_val,left_exhausted = getnext(left_iter)

def like(arg, pat, single_char='_', multi_wild='%'):
    'An string/pattern comparison function that uses a database style pattern'
    
    # The way this works is to covert the database style pattern to a regular expression
    x = re.sub('([][.*^$()])','\\\1',pat) #excape any re specific syntactic items that are in the pattern
    y = re.sub(multi_wild,'.*',x)
    z = re.sub(single_char,'.',y)
    return bool(re.fullmatch(z,arg))
    
    
def chomp(arg, chomp_char='\n'):
    '''
    Modeled after the perl function of the same name.
    Purpose is to remove new line characters from end of string during file processing.
    This fuction is meant to act on strings. Functionality with other data types that
    support array like access is undefined.
    '''
    if len(arg) >= len(chomp_char) and arg[-1*len(chomp_char):] == chomp_char:
        return arg[0:-1*len(chomp_char)] # IF the final character is a new line, then return everything up to that character
    return arg

def reduce2(function, sequence, initial=None, finisher=None):
    '''
    Support reduce operations that require a final step after the reduce has
    been performed.
    '''
    reduce_result=reduce(function,sequence,initial)
    if finisher:
        return finisher(reduce_result)
    return reduce_result
    
def reduce_avg(sequence, target=None):
    '''
    A reduce driven implementation of average that allows for the target field
    to be defined by a function
    '''
    m=map(nvl(target,lambda x:x),sequence)
    return reduce2(lambda x,y: (x[0] + y,x[1]+1) , m, (0,0), lambda x: x[0]/x[1])
   
   
def reduce_sum(sequence, target=None):
    '''
    A reduce driven implementation of sum that allows for the target field
    to be defined by a function
    '''
    m=map(nvl(target,lambda x:x),sequence)
    return reduce2(lambda x,y: x+y, m,0)
    
def group_aggregate_sum(target):
    return (lambda x,y:x+y,lambda:0,target,None)
    
def group_aggregate_avg(target): # I need to figure out how to implement a finisher function with this one
    return (lambda x,y:(x[0]+y,x[1]+1),lambda:(0,0),target,None)

def nmax(*y):
    '''
    An implementation of min which disregards any None values.
    Be aware that at least one none None value must be passed, otherwise
    a ValueError is raised by min
    '''
    return max(filter(lambda x:x!=None,y))

def group_aggregate_max(target):
    return (lambda x,y:nmax(x,y),lambda:None,target,None)
    
def nmin(*y):
    '''
    An implementation of min which disregards any None values.
    Be aware that at least one none None value must be passed, otherwise
    a ValueError is raised by min
    '''
    return min(filter(lambda x:x!=None,y))

def group_aggregate_min(target):
    return (lambda x,y:nmin(x,y),lambda:None,target,None)

group_aggregate_count = (lambda x,y:x+1,lambda:0,lambda x:None,None)
    
def group_by_proto(key, sequence, aggregate):
    '''
    This is the prototype of the group by function. It only allows the use of a single aggregate
    '''
    from collections import defaultdict
    def f(x,y):
        x[key(y)]=aggregate[0](x[key(y)],aggregate[2](y))
        return x
    return reduce2(f,sequence,defaultdict(aggregate[1]))
    
def group_by(key, sequence, *aggregates): # Need to implement a finisher
    '''
    A general aggregate grouping function that allows the processing of multiple 
    aggregates at the same time. The output is a dictionary whose keys reference
    a list of values (the aggregations).
    Aggregates are to be tuples (or tuple like) with four values: 
    1. The aggregate function
    2. Starting value
    3. Function defining the value to aggregate (usually a function that is able to isolate the value from a record)
    4. A finisher function if such applies (avg uses a finisher)
    The prebuilt aggregates already typically provide these items for you, except for #3
    '''

    def f(x,y):  # This is the function for reduce which will iterate through all the aggregations for each record processed.
        for i in range(len(aggregates)):
            x[key(y)][i]=aggregates[i][0](x[key(y)][i],aggregates[i][2](y))
        return x
    def d():  # This function is used to create the default value for the defaultdict
        l=list()
        for i in aggregates:
            l.append(i[1]())
        return l

    r = reduce2(f,sequence,defaultdict(d))
    #finalizer needs to go here.
    return r
 

def none_on_exception(call, exception_cls=None, *args,**kargs):
    '''
    The idea here is to provide a graceful and succinct way to handle exceptions
    that occur when executing a callable for which an exception is reasonably 
    expected and will be ignored. If an exception occurs then return None.
    Be forwarned, all exceptions will be caught.
    '''
    et=nvl(exception_cls,())
    try:
        return call(*args,**kargs)
    except et:
        return None
noe=none_on_exception  # A simply alias is in order for this one

##############################################################################
## Standard Data sets will appear below this line
## Most probably will place standard data sets in a separate module at some point
##############################################################################