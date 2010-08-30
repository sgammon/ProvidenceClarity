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


# Master meta-class for all P/C-related classes
class ProvidenceClarityObject(type):
    
    def __call__(metacls, name, bases, dictionary):
        return super(ProvidenceClarityObject, metacls).__call__(name, bases, dictionary)


# Controls the creation of the Platform class and object
class ProvidenceClarityPlatform(type):
    
    __metaclass__ = ProvidenceClarityObject
    
    def __new__(meta, classname, bases, classDict):
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
    
    __metaclass__ = ProvidenceClarityObject
    
    def __new__(meta, classname, bases, classDict):
        
        if '_subcontrollers' not in classDict:
            classDict['_subcontrollers'] = []
        if '_subcontroller_dispatch' not in classDict:
            classDict['_subcontroller_dispatch'] = {}
                            
        return type.__new__(meta, classname, bases, classDict)


# Parent to all platform proxy objects
class PCCoreProxy(object):

    def __repr__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __str__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __unicode__(self):
        return u'<CoreProxy "'+str(self.__class__.__name__)+'">'
        

# Proxies a PC controller into the platform object
class PCControllerProxy(PCCoreProxy):

    __metaclass__ = ProvidenceClarityController
    c_class = None

    def __init__(self, package_name, controller):
        if isinstance(controller, ProvidenceClarityController):
            self.c_class = controller()
            self.c_class.__api_package_name__ = package_name
        else:
            raise NotImplemented('Cannot proxy with non-compliant controller.') ## TODO: specific exception here
    
    def __get__(self, _instance, _class):
        return self.c_class
        
    def __set__(self, instance, value):
        raise NotImplemented('Platform controller properties are read-only.')
        
    def __delete__(self, instance):
        raise NotImplemented('Platform controller properties are read-only.')
        
        
# Proxies API requests to PCControllerProxies
_api_map = frozenset(['analyzer','cache','data','dev','index','input','media','output','security','storage','util'])
_api_dispatch = {}
class PCAPIProxy(PCCoreProxy):

    def __getattribute__(self, name):
        
        global _api_map
        global _api_dispatch

        if name not in _api_map:
            
            if not name[0:2] == '__':
                raise exceptions.APINotImplemented('Could not load API controller for given name "%s".' % name)
            else:
                return super(PCAPIProxy, self).__getattribute__(name)
                
        else:
            if name in _api_dispatch:
                return _api_dispatch[name].__get__(self, super(PCAPIProxy, self).__getattribute__('__class__'))
            else:
                try:
                    api_object = __import__('.'.join(['ProvidenceClarity','api',name]),globals(),locals(),['_controller'])
                    _api_dispatch[name] = PCControllerProxy(name, getattr(api_object, '_controller'))
                    return _api_dispatch[name].__get__(self, super(PCAPIProxy, self).__getattribute__('__class__'))
                except ImportError:
                    raise exceptions.APIInvalid('Could not load valid API controller for given name "%s", despite being found in API map.' % name)
        
    
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
            raise Exception('DAMN') ## @TODO: Real exception here
        
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
        

# Providence Clarity Platform!
class Platform(object):

    """
    
    =============================  Providence/Clarity  =============================
    
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
        -- config_path: Stores a path to P/C's config module. (r: string)
        -- namespace: The current operating namespace for GAE APIs. (r: string)
        -- api: Stores references to loaded API controllers. (r: dynamic module)
        -- services: Stores references to loaded service controllers. (r: module)
        
    Keyword Parameters:
        -- namespace: Sets the current namespace to this string value.
        
    
    """

    __metaclass__ = ProvidenceClarityPlatform

    ## ===== 1: Properties (Initialized Externally)
    version     = None
    namespace   = None    
    config      = None
    config_path = None
    clock       = None
    state       = None
    api         = None
    
    ## ===== 2: Internals
    __log_map = logging._levelNames

    ## ===== 3: Internal Methods
    def __init__(self,config='pc_config',**kwargs):
        
        ## Setup globals
        global version_major
        global version_minor
        global config_module
        global build
        
        version = {'major':version_major,'minor':version_minor,'full':str(version_major)+'.'+str(version_minor)+' '+str(build),'build':build}
        
        ## Path Inserts
        if '.' not in sys.path:
            sys.path.insert(0,'.')
            sys.path.insert(1,'lib')

        ## Load Config
        if config is False:
            raise exceptions.ConfigRequired()
        else:
            if isinstance(config, type(os)):
                config_mod = config
            elif isinstance(config, (str, unicode, basestring)):
                try:
                    config_mod = __import__('.'.join(['ProvidenceClarity',config]),globals(),locals(),['get','dump','config'],-1)
            
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
        
        ## Setup capabilities sets
        _cap = capabilities.CapabilitySet
        
        ## Setup object proxies
        self.api = PCAPIProxy()
        self.log = PCLogProxy()
        self.state = PCStateProxy()
        self.clock = PCClockProxy()
        self.config = config_mod
        
        ## Setup initial state
        self.state.set('env',os.environ)
        self.state.set('quotas', None)
        self.state.set('namespace',namespace_manager.get_namespace())
        self.state.set('capabilities', {'api':{
                                            'images':{'enabled':_cap('images').is_enabled(),'crop':_cap('images',methods=['crop']).is_enabled(),'get_serving_url':_cap('images',methods=['get_serving_url']).is_enabled(),'resize':_cap('images',methods=['resize']).is_enabled(),'rotate':_cap('images',methods=['rotate']).is_enabled()},
                                            'datastore_v3':{'enabled':_cap('datastore_v3').is_enabled(),'write':_cap('datastore_v3',capabilities=['write']).is_enabled(),'read':_cap('datastore_v3',capabilities=['read']).is_enabled()},
                                            'users':{'enabled':_cap('users').is_enabled(),'get_current_user':_cap('users',methods=['get_current_user']).is_enabled(),'is_current_user_admin':_cap('users',methods=['is_current_user_admin']).is_enabled()},
                                            'mail':{'enabled':_cap('mail').is_enabled(),'send_mail':_cap('mail',methods=['send_mail']).is_enabled(),'send_mail_to_admins':_cap('mail',methods=['send_mail_to_admins']).is_enabled()},
                                            'memcache':{'enabled':_cap('memcache').is_enabled(),'get':_cap('memcache',methods=['get']).is_enabled(),'set':_cap('memcache',methods=['set']).is_enabled(),'delete':_cap('memcache',methods=['delete']).is_enabled()},
                                            'oauth':{'enabled':_cap('oauth').is_enabled(),'get_current_user':_cap('oauth',methods=['get_current_user']).is_enabled(),'is_current_user_admin':_cap('oauth',methods=['is_current_user_admin']).is_enabled()},
                                            'multitenancy':{'enabled':_cap('multitenancy').is_enabled(),'get_namespace':_cap('multitenancy',methods=['get_namespace']).is_enabled(),'set_namespace':_cap('multitenancy',methods=['set_namespace']).is_enabled()},
                                            'blobstore':{'enabled':_cap('blobstore').is_enabled(),'get':_cap('blobstore',methods=['get']).is_enabled(),'delete':_cap('blobstore',methods=['delete']).is_enabled()},
                                            'xmpp':{'enabled':_cap('xmpp').is_enabled(),'send_message':_cap('xmpp',methods=['send_message']).is_enabled(),'send_invite':_cap('xmpp',methods=['send_invite']).is_enabled()},                         
                                            'urlfetch':{'enabled':_cap('urlfetch').is_enabled(),'fetch':_cap('urlfetch',methods=['fetch']).is_enabled()}
                                            }
                                        })
                    
        # :: Namespace is usually extracted from subdomain - set via initialized keyword parameter
        if self.config.get('enable','multitenancy',False):
            
            _m_log = self.config.get('logging','multitenancy',False)
            
            if self.config.get('force_namespace','multitenancy', False):
                if isinstance(self.config.get('force_namespace','multitenancy',False), (str, unicode)) and self.config.get('force_namespace','multitenancy',False) is not '':
                    if namespace_manager.validate_namespace(self.config.get('force_namespace','multitenancy',False)):

                        if _m_log: logging.info('[i]: Setting request namespace to \''+config_get('force_namespace','multitenancy',False)+'\'.')
                        namespace_manager.set_namespace(self.config.get('force_namespace','multitenancy',False))
            
            else:
            
                if 'namespace' in kwargs or self.config.get('apps_mode_force', 'multitenancy', False):
                    if kwargs['namespace'] == self.config.get('apps_subdomain','multitenancy','apps') or self.config.get('apps_mode_force', 'multitenancy', False):

                        if _m_log: logging.info('[i]: Setting request namespace to \''+namespace_manager.google_apps_namespace()+'\' per APPS procedure.')
                        namespace_manager.set_namespace(namespace_manager.google_apps_namespace())

                    else:
                        if isinstance(kwargs['namespace'], (str, unicode)) and namespace_manager.validate_namespace(kwargs['namespace']):

                            if _m_log: logging.info('[i]: Setting request namespace to \''+kwargs['namespace']+'\' per domain split procedure.')
                            namespace_manager.set_namespace(kwargs['namespace'])
                            
                        else:
                            if kwargs['namespace'] is not None:
                                if _m_log: logging.info('[i]: Given namespace \''+str(kwargs['namespace'])+'\' failed to pass validation. Ignoring.')

        if 'version' in kwargs:
            self.version = kwargs['version']
        else:
            self.version = version
        
        super(Platform, self).__init__()
    
    ## ===== 4: Class Methods
    @classmethod
    def config(cls):
        return cls.config

    @classmethod
    def version(cls):
        return cls.version
        
    
## Master Controller Object
class PCController(object):

    __metaclass__ = ProvidenceClarityController
       
    def __getattr__(self, name):

        super_obj = super(PCController, self)

        if name in super(PCController, self).__getattribute__('_subcontrollers'):
            api_package_name = super_obj.__getattribute__('__api_package_name__')
            stack = ['ProvidenceClarity','api',api_package_name] + super(PCController, self).__getattribute__('_subcontrollers')[name]

            api_object = __import__('.'.join(stack[0:-1]),globals(),locals(),[-1])
            self._subcontroller_dispatch[name] = PCControllerProxy(name, getattr(api_object, stack[-1]))
            return self._subcontroller_dispatch[name].__get__(self, super(PCController, self).__getattribute__('__class__'))
        else:
            return super_obj.__getattribute__(name)
        
    """
    def __getattribute__(self, name):
        soop = super(PCController, self)
        if hasattr(self, '_subcontrollers') and soop.__getattribute__('_subcontrollers') is not None:
            if name in soop.__getattribute__('_subcontrollers_dispatch'):
                return soop.__getattribute__('_subcontrollers_dispatch')[name].__get__(self, self.__class__)
            else:
                if isinstance(self._subcontrollers, dict):
                    if name in self._subcontrollers.keys():
                        soop._subcontrollers_dispatch[name] = soop.__getattribute__('_subcontrollers')[name]()
                        return soop.__getattribute__('_subcontrollers_dispatch')[name]
                    else:
                        raise exceptions.APIInvalid('Could not load subcontroller "%s".' % name)
                else:
                    exceptions.APIInvalid('Could not load subcontroller from invalid dispatcher (of type "%s").' % str(type(soop.__getattribute__('_subcontrollers_dispatch'))))
        return soop.__getattribute__(name)
    """
    

# Log controller for logging
class PCLogProxy(PCController):
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

## Init and return a ProvidenceClarity object
def initialize(platform_profile=None,namespace=None,config='pc_config'):

    if platform_profile is not None:
        if isinstance(platform_profile, ProvidenceClarityPlatform):
            p = platform_profile(namespace=namespace,config=config)
    else:
        p = Platform(config)
    return p