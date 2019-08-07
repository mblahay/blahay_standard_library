def regexp_like(args, argp):
    '''
    A simply simple wrapper around the re.search function. The result
    of that function will be converted to a binary True/False.
    
    This function will return a simple True or False, no match object.
    '''
    from re import search 
    return bool(search(argp, args)) # Simply execute the search method using the string and pattern, 
                                    # then interpret the existance of a returned match object into 
                                    # a True of False using the bool constructor.

def regexp_substr():
    pass

def regexp_replace():
    pass