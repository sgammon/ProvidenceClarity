import logging
from ProvidenceClarity import pc_config

do_logging = pc_config.get('import_logging', 'api.util', False)

def import_helper(name, fromlist=None):
    
    global do_logging
    
    if do_logging: logging.debug('Import logging turned on for api.util.')
    if do_logging: logging.debug('Import request for name: "%s" with fromlist "%s".' % name, str(fromlist))
    
    try:
        
        if fromlist is None:
            
            if isinstance(name, list):
                mod = __import__('.'.join(name))
            elif isinstance(name, str):
                mod = __import__(name)
            else:
                return False
                
            if do_logging: logging.debug('Import request successful. Returning "%s".' % str(mod))

        else:
            
            if isinstance(fromlist, str):
                fromlist = [fromlist]
            
            if isinstance(name, list):
                mod = __import__('.'.join(name), globals(), locals(), fromlist)
                
            elif isinstance(name, str):
                
                mod = __import__(name, globals(), locals, fromlist)
                
            mod_properties = {}
            for prop in fromlist:
                mod_properties[prop] = getattr(mod, prop)
            
            enum_props = []
            index_props = {}
             
            for prop in fromlist:
                item = getattr(mod, prop)
                enum_props.append(item)
                index_props[prop] = item
            
            if do_logging: logging.debug('Import request successful. Returning (with props) "%s".' % str(mod))
                            
            return (mod, {'list':enum_props,'dict':index_props})
                            
        
    except ImportError:
        #@TODO: Find a way to store errors in the datastore
        if do_logging: logging.error('ImportError caught. Returning False.')
        return False
        
    finally:
        if do_logging: logging.debug('Import request finished.')