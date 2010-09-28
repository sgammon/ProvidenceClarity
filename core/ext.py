import exceptions
from . import PCCoreProxy
from ProvidenceClarity.api.util import import_helper


# Allows the ext prop to operate normally without a platform instance
class PCExtProxyResponder(type):

    _ext_points = { 'Receiver':['api','input','receiver','ReceiverAdapter'],
                    'Fetcher':['api','input','fetcher','FetchAdapter'],
                    
                    'Service':['api','services','ServiceAdapter'],
                    
                    'Viewer':['api','output','viewer','ViewAdapter'],
                    'Grapher':['api','output','grapher','GraphAdapter'],
                    
                    'DataManager':['api','data','DataManager'],

                    'Attribute':['data','attribute','A'],
                    'Cache':['data','cache','C'],
                    'NormalizedCache':['data','cache','NC'],
                    'Descriptor':['data','descriptor','D'],
                    'Entity':['data','entity','E'],
                    'Index':['data','index','I'],
                    'NormalizedIndex':['data','index','NI'],
                    'Prototype':['data','proto','P'],
                    'Relation':['data','proto','R']
                }
                    
    _ext_dispatch = {}    
    
    def __new__(meta, classname, bases, classDict, *args, **kwargs):
        
        if '_ext_points' not in classDict:
            classDict['_ext_points'] = PCExtProxyResponder._ext_points
            classDict['_ext_dispatch'] = PCExtProxyResponder._ext_dispatch
        
        return type.__new__(meta, classname, bases, classDict)
        
    def __getattribute__(self, name):
        
        soop = super(PCExtProxyResponder, self)
        _ext_map = soop.__getattribute__('_ext_points')
        _ext_dispatch = soop.__getattribute__('_ext_dispatch')
        
        if name not in _ext_map:
            
            if not name[0] == '_':
                raise exceptions.ExtensionNotImplemented('Could not load extension point for given name "%s".' % name)
            else:
                return super(PCExtProxyResponder, self).__getattribute__(name)
                
        else:
            
            if name in _ext_dispatch:
                return _ext_dispatch[name]
            else:
                try:
                    package = ['ProvidenceClarity']+_ext_map[name]
                    ext_object, props = import_helper(package[0:-1],package[-1])
                    _ext_dispatch[name] = props['dict'][package[-1]]
                    
                    return _ext_dispatch[name]
                    
                except ImportError:
                    raise exceptions.ExtensionInvalid('Could not load valid extension class for given name "%s", despite being found in EXT map.' % name)        


# Easy access point for all extension points in P/C
class PCExtProxy(PCCoreProxy):

    __metaclass__ = PCExtProxyResponder
        
    def __getattribute__(self, name):
        
        soop = super(PCExtProxy, self)
        _ext_map = soop.__getattribute__('_ext_points')
        _ext_dispatch = soop.__getattribute__('_ext_dispatch')
        
        if name not in _ext_map:
            
            if not name[0] == '_':
                raise exceptions.ExtensionNotImplemented('Could not load extension point for given name "%s".' % name)
            else:
                return super(PCExtProxy, self).__getattribute__(name)
                
        else:
            
            if name in _ext_dispatch:
                return _ext_dispatch[name]
            else:
                try:
                    package = ['ProvidenceClarity']+_ext_map[name]
                    ext_object, props = import_helper(package[0:-1],package[-1])
                    _ext_dispatch[name] = props['dict'][package[-1]]
                    
                    return _ext_dispatch[name]
                    
                except ImportError:
                    raise exceptions.ExtensionInvalid('Could not load valid extension class for given name "%s", despite being found in EXT map.' % name)
