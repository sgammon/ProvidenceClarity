
def import_helper(name, fromlist=None):
    
    try:
        
        if fromlist == None:
            mod = __import__(name)

        elif isinstance(fromlist, list):
            
            if len(fromlist) == 1:
                mod = __import__(name+'.'+fromlist[0])

            elif len(fromlist) > 1:
                mod = __import__(name+'.'+'.'.join(fromlist))

        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        
        return mod
        
    except ImportError:
        #TODO: Find a way to store errors in the datastore
        return False