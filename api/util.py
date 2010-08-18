import logging

def import_helper(name, fromlist=None):
    
    try:
        
        if fromlist is None:
            mod = __import__(name)

        else:
            if isinstance(fromlist, list):
                fromlist = str(fromlist[0])

            class_path_t = name.split('.')
            class_path_t.append(fromlist)
            
            mod = __import__('.'.join(class_path_t[0:-1]), globals(), locals(), class_path_t[-1], -1)
            mod = getattr(mod, class_path_t[-1])
            
        return mod
        
    except ImportError:
        #TODO: Find a way to store errors in the datastore
        return False