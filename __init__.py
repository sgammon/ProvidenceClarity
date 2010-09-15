#
#   =====================================================
#   |==|  PROVIDENCE/CLARITY DATA ANALYSIS PLATFORM  |==|
#   |==|     -----------------------------------     |==|
#   |==| Author: Sam Gammon <sg@samgammon.com>       |==|
#   |==| Version: 0.1 DEV                            |==|
#   |==| ------------------------------------------- |==|
#   |==|   COPYRIGHT (c) 2010. ALL RIGHTS RESERVED   |==|
#   =====================================================
#

import os, sys, logging, exceptions, datetime
from google.appengine.api import namespace_manager, quota, capabilities

from ProvidenceClarity.api.util import import_helper

## Import Details
__all__ = ['Platform']
__protos__ = ['data']

## Declare Globals
version_major = '0.1'
version_minor = '6.000'
config_module = None
build = 'DEV'

## Expose Import-able Variables
VERSION = str(version_major)+'.'+str(version_minor)+' '+str(build)
PC_PATH = os.path.join(os.path.dirname(__file__))
    

# Master ancestor class for all P/C-related classes
class ProvidenceClarityObject(object):
    pass


# Controls the creation of the Platform class and object
class ProvidenceClarityPlatform(type):
    
    def __new__(meta, classname, bases, classDict, *args, **kwargs):
        return type.__new__(meta, classname, bases, classDict)
        
    def _platformName(self):
        return self.__name__
        
    def __repr__(self):
        return '<ProvidenceClarityPlatform "%s">' % self._platformName()
        
    def __str__(self):
        return '<ProvidenceClarityPlatform "%s">' % self._platformName()
        
    def __unicode__(self):
        return u'<ProvidenceClarityPlatform "%s">' % self._platformName()
    
        
# Controls the loading and creation of PC Controllers and proxies
class ProvidenceClarityController(type):
    
    def __new__(meta, classname, bases, classDict):
        
        if '_subcontrollers' not in classDict:
            classDict['_subcontrollers'] = []
        if '_subcontroller_dispatch' not in classDict:
            classDict['_subcontroller_dispatch'] = {}
                            
        return type.__new__(meta, classname, bases, classDict)
        

# Bridges a 'platform' property over to other objects
class PCPlatformBridge(object):
    
    platform = None
    
    def _setPlatformParent(self, platform):
        super(PCPlatformBridge, self).__setattr__('platform', platform)
        
        
# Parent to all platform proxy objects
class PCCoreProxy(ProvidenceClarityObject, PCPlatformBridge):
    
    def __repr__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __str__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __unicode__(self):
        return u'<CoreProxy "'+str(self.__class__.__name__)+'">'        
        

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
        
        
# Proxies a PC controller into the platform object
class PCControllerProxy(PCCoreProxy):

    __metaclass__ = ProvidenceClarityController
    c_class = None

    def __init__(self, package_name, controller):
        
        if isinstance(controller, ProvidenceClarityController):
            self.c_class = controller()
            self.c_class.__api_package_name__ = package_name
        else:
            raise exceptions.InvalidController('Cannot proxy with non-compliant controller.') ## TODO: specific exception here
    
    def __get__(self, _instance, _class):
        return self.c_class
        
    def __set__(self, instance, value):
        raise NotImplemented
        
    def __delete__(self, instance):
        raise NotImplemented
        

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
        
    
# Platform to store state information and key=>values for later use        
_state_object = {}
class PCStateProxy(PCCoreProxy):
        
    def __init__(self, state=None):
        global _state_object
        if state is not None:
            if isinstance(state, dict):
                for item in state:
                    _state_object[item] = state[item]
            
    def __getattr__(self, name):
        global _state_object
        if isinstance(_state_object, dict):
            if name in _state_object:
                return _state_object[name]
                    
    def __setattr__(self, name, value):
        global _state_object
        if isinstance(_state_object, dict):
            _state_object[name] = value
        else:
            _state_object = {name:value}
        
    def set(self, name, value):
        global _state_object
        if isinstance(_state_object, dict):
            _state_object[name] = value
            
    def get(self, name):
        global _state_object
        if isinstance(_state_object, dict):
            if name in _state_object:
                return _state_object[name]
            else:
                return None
        else:
            return None


# Clock object measures timepoints for debugging/etc.
class PCClockProxy(PCCoreProxy):
    
    _clock = []
    
    def __init__(self):
        self.timepoint('boot')
            
    def timepoint(self, name):
        time_value = datetime.datetime.now()
        self._clock.append((name, {'time':time_value, 'cpu':quota.get_request_cpu_usage(), 'cpu_api':quota.get_request_api_cpu_usage()}))
        return True
        
    def dump(self):
        return _clock      
        
        
# Log controller for logging
class PCLogProxy(PCCoreProxy):
    
    logger_queue = []
    
    # Logger wrapper, based on current config
    def log(self,message_i, level='debug'):
        
        if __log_map[str(self.config().get('threshold','logging')).upper()] >= __log_map[str(level).upper()]:
            
            handler = self.config().get('handler','logging')
            message = str(message_i)

            if self.config().get('tag','logging') == True:
                message = message + ' (Providence/Clarity v'+str(self.version)+')'

            result = getattr(handler,str(level).lower())(message)
            
        else:
            return None
    
    # Log wrapper for debug
    def debug(self, message):
        return self.log(message,'debug')

    # Log wrapper for info
    def info(self, message):
        return self.log(message,'info')
        
    # Log wrapper for warning
    def warning(self, message):
        return self.log(message,'warning')
        
    # Log wrapper for error
    def error(self, message):
        return self.log(message,'error')
        
    # Log wrapper for critical
    def critical(self, message):
        return self.log(message,'critical')
        
    # Log wrapper for exit
    def exit(self, message):
        return self.log(message,'exit')         
          

# Proxies requests for config items (mainly done for consistency with other platform proxies)
class PCConfigProxy(PCCoreProxy):

    _c_module = None # Stores reference to pc_config module
    _c_data = None # Stores copy of config data for later switch to using this class (@TODO: Switch to universal config )

    def setConfig(self, config):
        self._c_module = config
        self._c_data = config.config
    
    def get(self, key, module, default=None):
        return self._c_module.get(key, module, default)
        
    def dump(self):
        return self._c_module.dump()
        
    
# Providence Clarity Platform!
class Platform(ProvidenceClarityObject):

    """
    
    ==================================  Providence/Clarity  ==================================
    
    Main Class:
        Everything is initialized and operated on from this master class,
        which stores references to internal APIs and handlers.
    
    Properties:
        -- version: Stores a dict of version values for P/C.
            -- full: A string of the system's full version. (ex: 0.5.131 DEV, r: string)
            -- major: The system's 'major' version. (ex: 0.5, r: int/float)
            -- minor: The system's 'minor' version. (ex: 131, r: int/float)
            -- build: The system's build release type. (ex: DEV, r: string)
        -- config: Stores a ref to P/C's config module (most useful for config.get, r: module)
        -- config_p: Stores a path to P/C's config module. (r: string)
        -- namespace: The current operating namespace for GAE APIs. (r: string)
        -- api: Stores references to loaded API controllers. (r: dynamic module)
        -- state: Stores registry-like (key=>value) information for later use (r: varies)
        -- clock: Measures and stores timepoints taken during runtime, along with cpu and cpu_api usage.
        
    Keyword Parameters:
        -- namespace: Sets the current namespace to this string value.
        -- version: Overrides the computed version for the platform.
        
        
    
    """

    __metaclass__ = ProvidenceClarityPlatform

    ## ===== 1: Properties/Platform Extension Proxies (Initialized Externally)
    config      = PCConfigProxy
    log         = PCLogProxy
    clock       = PCClockProxy
    state       = PCStateProxy
    api         = PCAPIProxy
    ext         = PCExtProxy
    
    ## ===== 2: Internals
    __log_map = logging._levelNames

    ## ===== 3: Internal Methods
    def __init__(self,config='pc_config', *args, **kwargs):
        
        ## Setup globals
        global version_major
        global version_minor
        global config_module
        global import_item
        global build
        
        version = {'major':version_major,'minor':version_minor,'full':str(version_major)+'.'+str(version_minor)+' '+str(build),'build':build}
        
        ## Path Inserts
        if '.' not in sys.path:
            sys.path.insert(0,'.')
            sys.path.insert(1,'lib')
            sys.path.insert(2, 'distlib')

        ## Setup capabilities sets
        _cap = capabilities.CapabilitySet
        
        ## Setup object proxies
        self.api = PCAPIProxy()
        self.log = PCLogProxy()
        self.state = PCStateProxy()
        self.clock = PCClockProxy()
        self.ext = PCExtProxy()
        self.config = PCConfigProxy()
        
        ## Link up with Platform
        self.api._setPlatformParent(self)
        self.log._setPlatformParent(self)
        self.state._setPlatformParent(self)
        self.clock._setPlatformParent(self)
        self.ext._setPlatformParent(self)
        self.config._setPlatformParent(self)
        
        ## Setup initial state
        self.state.set('env',os.environ)
        self.state.set('quotas', None)
        self.state.set('namespace',namespace_manager.get_namespace())
        self.state.set('capabilities', {'api':{
                                            'images':{
                                                'enabled':_cap('images').is_enabled(),
                                                'crop':_cap('images',methods=['crop']).is_enabled(),
                                                'get_serving_url':_cap('images',methods=['get_serving_url']).is_enabled(),
                                                'resize':_cap('images',methods=['resize']).is_enabled(),
                                                'rotate':_cap('images',methods=['rotate']).is_enabled()},
                                            'datastore_v3':{
                                                'enabled':_cap('datastore_v3').is_enabled(),
                                                'write':_cap('datastore_v3',capabilities=['write']).is_enabled(),
                                                'read':_cap('datastore_v3',capabilities=['read']).is_enabled(),
                                                'put':_cap('datastore_v3',methods=['put']).is_enabled(),
                                                'delete':_cap('datastore_v3',methods=['delete']).is_enabled(),
                                                'get':_cap('datastore_v3',methods=['get']).is_enabled(),
                                                'run_in_transaction':_cap('datastore_v3',methods=['run_in_transaction']).is_enabled(),
                                                'run_in_transaction_custom_retries':_cap('datastore_v3',methods=['run_in_transaction']).is_enabled()},
                                            'users':{
                                                'enabled':_cap('users').is_enabled(),
                                                'get_current_user':_cap('users',methods=['get_current_user']).is_enabled(),
                                                'is_current_user_admin':_cap('users',methods=['is_current_user_admin']).is_enabled()},
                                            'mail':{
                                                'enabled':_cap('mail').is_enabled(),
                                                'send_mail':_cap('mail',methods=['send_mail']).is_enabled(),
                                                'send_mail_to_admins':_cap('mail',methods=['send_mail_to_admins']).is_enabled()},
                                            'memcache':{
                                                'enabled':_cap('memcache').is_enabled(),
                                                'get':_cap('memcache',methods=['get']).is_enabled(),
                                                'set':_cap('memcache',methods=['set']).is_enabled(),
                                                'delete':_cap('memcache',methods=['delete']).is_enabled()},
                                            'oauth':{
                                                'enabled':_cap('oauth').is_enabled(),
                                                'get_current_user':_cap('oauth',methods=['get_current_user']).is_enabled(),
                                                'is_current_user_admin':_cap('oauth',methods=['is_current_user_admin']).is_enabled()},
                                            'multitenancy':{
                                                'enabled':_cap('multitenancy').is_enabled(),
                                                'get_namespace':_cap('multitenancy',methods=['get_namespace']).is_enabled(),
                                                'set_namespace':_cap('multitenancy',methods=['set_namespace']).is_enabled()},
                                            'blobstore':{
                                                'enabled':_cap('blobstore').is_enabled(),
                                                'get':_cap('blobstore',methods=['get']).is_enabled(),
                                                'delete':_cap('blobstore',methods=['delete']).is_enabled()},
                                            'xmpp':{
                                                'enabled':_cap('xmpp').is_enabled(),
                                                'send_message':_cap('xmpp',methods=['send_message']).is_enabled(),
                                                'send_invite':_cap('xmpp',methods=['send_invite']).is_enabled()},                         
                                            'urlfetch':{
                                                'enabled':_cap('urlfetch').is_enabled(),
                                                'fetch':_cap('urlfetch',methods=['fetch']).is_enabled()}
                                            }
                                        })
                                        

        ## Load Config
        if config is False or config == '' or config is None:
            raise exceptions.ConfigRequired()
        else:
            if isinstance(config, type(os)):
                self.config.setConfig(config)
            else:
                try:
                    config_mod, props = import_helper(['ProvidenceClarity',config],['get','dump','config'])
                    self.config.setConfig(config_mod)
            
                except ImportError: raise exceptions.InvalidConfig()
        
        
        ## Environment Vars - Split for Namespace
        software_t = '/'.split(os.environ['SERVER_SOFTWARE'])
        if software_t[0].lower() == 'development': platform = 'Dev';
        else: platform = 'Production'
    
        domain = os.environ['HTTP_HOST'].split(':')[0].split('.')
        if domain[-1] == 'com':
            subdomain = domain[0]
        else:
            subdomain = None                                        
                    
        # :: Namespace is usually extracted from subdomain - set via initialized keyword parameter
        if self.config.get('enable','multitenancy',False):
            
            _m_log = self.config.get('logging','multitenancy',False)
            
            if self.config.get('force_namespace','multitenancy', False):
                if isinstance(self.config.get('force_namespace','multitenancy',False), (str, unicode)) and self.config.get('force_namespace','multitenancy',False) is not '':
                    if namespace_manager.validate_namespace(self.config.get('force_namespace','multitenancy',False)):

                        if _m_log: self.log.info('Setting request namespace to "%s".' % config_get('force_namespace','multitenancy',False))
                        namespace_manager.set_namespace(self.config.get('force_namespace','multitenancy',False))
            
            else:
            
                if 'namespace' in kwargs or self.config.get('apps_mode_force', 'multitenancy', False):
                    if kwargs['namespace'] == self.config.get('apps_subdomain','multitenancy','apps') or self.config.get('apps_mode_force', 'multitenancy', False):

                        if _m_log: self.log.info('Setting request namespace to Google Apps domain "%s".' % namespace_manager.google_apps_namespace())
                        namespace_manager.set_namespace(namespace_manager.google_apps_namespace())

                    else:
                        if isinstance(kwargs['namespace'], (str, unicode)) and namespace_manager.validate_namespace(kwargs['namespace']):

                            if _m_log: self.log.info('Setting request namespace to split domain "%s".' % kwargs['namespace'])
                            namespace_manager.set_namespace(kwargs['namespace'])
                            
                        else:
                            if kwargs['namespace'] is not None:
                                if _m_log: self.log.info('Given namespace "%s" failed to pass validation. Ignoring.' % str(kwargs['namespace']))

        if 'version' in kwargs:
            self.version = kwargs['version']
        else:
            self.version = version
        
        super(Platform, self).__init__(*args, **kwargs)
    
    
    def __repr__(self):
        return '<ProvidenceClarityPlatform "%s">' % self.__class__.__name__
        
    def __str__(self):
        return '<ProvidenceClarityPlatform "%s">' % self.__class__.__name__
        
    def __unicode__(self):
        return u'<ProvidenceClarityPlatform "%s">' % self.__class__.__name__
    
    ## ===== 4: Class Methods
    @classmethod
    def config(cls):
        return cls.config

    @classmethod
    def version(cls):
        return cls.version
            
    
## Master Controller Object
class PCController(ProvidenceClarityObject):

    __metaclass__ = ProvidenceClarityController
       
    def __getattr__(self, name):

        super_obj = super(PCController, self)

        if name in super(PCController, self).__getattribute__('_subcontrollers'):
            api_package_name = super_obj.__getattribute__('__api_package_name__')
            stack = ['ProvidenceClarity','api',api_package_name] + super(PCController, self).__getattribute__('_subcontrollers')[name]

            api_object, props = import_helper(stack[0:-1],stack[-1])
            
            self._subcontroller_dispatch[name] = PCControllerProxy(name, props['dict'][stack[-1]])
            return self._subcontroller_dispatch[name].__get__(self, super(PCController, self).__getattribute__('__class__'))
        else:
            return super_obj.__getattribute__(name)
            

## Adapter object for incoming/outgoing adapters
class PCAdapter(ProvidenceClarityObject):

    def adapt(self, input=None):
        pass
        

## Init and return a ProvidenceClarity object
def initialize(platform_profile=None,namespace=None,config='pc_config'):

    if platform_profile is not None:
        if isinstance(platform_profile, ProvidenceClarityPlatform):
            p = platform_profile(namespace=namespace,config=config)
    else:
        p = Platform(config)
    return p