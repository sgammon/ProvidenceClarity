import logging, exceptions
from . import PCCoreProxy
from controller import PCControllerProxy
from ProvidenceClarity.api.util import import_helper

# Allows the proxy parameter to work normally without a platform instance
class PCAPIProxyResponder(type):

    _api_map = frozenset(['analyzer','cache','data','dev','index','input','media','output','security','services','storage','util'])
    _api_dispatch = {}
    
    def __new__(meta, classname, bases, classDict, *args, **kwargs):
        
        if '_api_map' not in classDict:
            classDict['_api_map'] = PCAPIProxyResponder._api_map
            classDict['_api_dispatch'] = PCAPIProxyResponder._api_dispatch    

        return type.__new__(meta, classname, bases, classDict)
        
    def __getattribute__(self, name):
        
        soop = super(PCAPIProxyResponder, self)
        _api_map = soop.__getattribute__('_api_map')
        _api_dispatch = soop.__getattribute__('_api_dispatch')
        
        if name not in _api_map:
            
            if not name[0] == '_':
                raise exceptions.APINotImplemented('Could not load API controller for given name "%s".' % name)
            else:
                return super(PCAPIProxy, self).__getattribute__(name)
                
        else:
            
            if name in _api_dispatch:
                return _api_dispatch[name].__get__(self, super(PCAPIProxyResponder, self).__getattribute__('__class__'))
            else:
                try:
                    api_object, props = import_helper(['ProvidenceClarity','api',name],['_controller'])
                    
                    _api_dispatch[name] = PCControllerProxy(name, props['dict']['_controller'])
                    return _api_dispatch[name].__get__(self, super(PCAPIProxyResponder, self).__getattribute__('__class__'))
                    
                except ImportError:
                    raise exceptions.APIInvalid('Could not load valid API controller for given name "%s", despite being found in API map.' % name)


# Proxies API requests to PCControllerProxies
class PCAPIProxy(PCCoreProxy):
    
    __metaclass__ = PCAPIProxyResponder

    def __getattribute__(self, name):
        
        soop = super(PCAPIProxy, self)
        _api_map = soop.__getattribute__('_api_map')
        _api_dispatch = soop.__getattribute__('_api_dispatch')
        
        if name not in _api_map:
            
            if not name[0] == '_':
                raise exceptions.APINotImplemented('Could not load API controller for given name "%s".' % name)
            else:
                return super(PCAPIProxy, self).__getattribute__(name)
                
        else:
            
            if name in _api_dispatch:
                return _api_dispatch[name].__get__(self, super(PCAPIProxy, self).__getattribute__('__class__'))
            else:
                try:
                    api_object, props = import_helper(['ProvidenceClarity','api',name],['_controller'])
                    
                    _api_dispatch[name] = PCControllerProxy(name, props['dict']['_controller'])
                    return _api_dispatch[name].__get__(self, super(PCAPIProxy, self).__getattribute__('__class__'))
                    
                except ImportError:
                    raise exceptions.APIInvalid('Could not load valid API controller for given name "%s", despite being found in API map.' % name)
