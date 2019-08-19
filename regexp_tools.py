import re
import itertools
import blahay_standard_library as bsl

def regexp_like(args, argp):
    '''
    A simple wrapper around the re.search function. The result
    of that function will be converted to a binary True/False.
    
    This function will return a simple True or False, no match object.

    Parameters:
    -----------
    args - This is the string argument which is to be searched.

    argp - This is the pattern that is used when searching args
    '''
    return bool(re.search(argp, args)) # Simply execute the search method using the string and pattern, 
                                       # then interpret the existance of a returned match object into 
                                       # a True of False using the bool constructor.

def regexp_substr():
    pass

def regexp_replace():
    pass

def regexp_parse(args, pat):
    '''
    Separate the string args by pat and denote which elements are 
    a pattern match and which ones are not.
    '''

    x=zip(re.split(pat,args),itertools.repeat(False))
    y=zip(re.findall(pat,args),itertools.repeat(True))
    return bsl.interleave(x,y)
