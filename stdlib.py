# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 09:57:12 2018

@author: mb18433
"""
import math
import itertools

def nvl(arg,alt_val=None): # Similar concept to NVL function available in Oracle databases
    'Allows for the substition of a value should the passed in argument be None.'
    if arg == None:
        return alt_val
    return arg
    
def zil(arg,alt_val=None): #zil stands for "zero item list," though the method works with anything that you can use len() with
    'Allows for the substitution of value if passed in argument has a length of zero'
    if len(arg) == 0:
        return alt_val
    return arg
    
def select(fields, record):
    'Returns a version of the dict record with only the designated fields. If field does not exist, then new dict key is assigned a value of None'
    return {x:record.get(x) for x in fields}

def anyin(l1,l2):
    # return any([ x in l2 for x in l1]) #Could use this, but decided to write logic to short circuit the process
    for i in l1:
        if i in l2:
            return True        
    return False        

def nfunc(arg, function = None, nfunction = None, nval = None):
    if arg:
        if function:
            return function(arg)
        else:
            return arg
    else:
        if nfunction:
            return nfunction(arg)
        else:
            return nval
        
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
    
##############################################################################
## Standard Data sets will appear below this line
## Most probably will place standard data sets in a separate module at some point
##############################################################################