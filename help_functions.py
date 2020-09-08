def reemovNestings(lst, flatlist): 
    l = lst
    for i in l: 
        if type(i) == list: 
            reemovNestings(i, flatlist) 
        else: 
            flatlist.append(i)
           