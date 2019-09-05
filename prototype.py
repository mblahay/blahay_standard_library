
def deepmap(func,nested_container, containers_types=[list,tuple]):
    '''
    Provides mapping capability across a nested data structure. Modeled after
    the map built-in, when provided with the nested container types, will 
    recurse into those data structures and apply the map function.
    '''    
    for i in nested_container:
        yield type(i)(deepmap(func,i)) if type(i) in containers_types else func(i)


def deepmap2(func,nested_container, containers_types=[list,tuple]):
    '''
    Provides mapping capability across a nested data structure. Modeled after
    the map built-in, when provided with the nested container types, will 
    recurse into those data structures and apply the map function.
    
    This version uses the built in map function in the recursion
    '''    
    return map(lambda x:      type(x)(deepmap2(func,x,containers_types=containers_types)) 
                           if type(x) in containers_types 
                         else func(x) 
              ,nested_container)
