#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 08:56:17 2019

@author: mblahay
"""

def list_index_cond(l,pred):
    '''
    This function provides a similar functionality to the index method of the 
    list class, but instead of searching for the first instance of a value 
    starting at the beginning, list_index_cond searches for the first instance
    where the predecate is true.
    
    Parameters:
        l - list that is being searched
        pred - predecate to be evaluated for each value. This must be a function
               that accepts a single parameter. The return value will be
               evaluated to True or False.
    '''
    for n,t in enumerate(l):
        if pred(t):
            return n
    return None
        
def list_get(l,ind):
    '''
    Provides list access similar to the get function of dict class. If the
    given index does not exist in the list, None is returned.
    '''
    try:
        return l[ind]
    except IndexError:
        return None
    
def list_get_wrap(l,ind):
    '''
    A modification of list_get which allows index parameters to wrap around to 
    the beginning and end of the available index range. What this means is that
    for a list with a final index value of 10, if one requests 11, the reference
    will wrap around to the beginning and return the first element.
    '''
    try:
        return l[ind]
    except IndexError:
        return l[ind % len(l)]
    
def list_index_get(l,ind):
    try:
        l.index(ind)
    except ValueError:
        return None
        