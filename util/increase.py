def nextend(lst, n):
    """ Pass in a list and append it to itself n times. 
    
    return
        The new list
    """
    nl = []
    for i in range(n):
        nl.extend(lst)
    return nl

