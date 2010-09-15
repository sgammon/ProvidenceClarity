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

import os
import logging
import exceptions

from google.appengine.api import namespace_manager


# Master meta-class for all P/C-related classes
class ProvidenceClarityObject(type):
    
    def __call__(metacls, name, bases, dictionary):
        return super(ProvidenceClarityObject, metacls).__call__(name, bases, dictionary)
        

# Controls the creation of the Platform class and object
class ProvidenceClarityPlatform(type):
    
    __metaclass__ = ProvidenceClarityObject
    
    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)
    

# Controls the loading and creation of PC Controllers and proxies
class ProvidenceClarityController(type):
    
    __metaclass__ = ProvidenceClarityObject
    
    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)
        

# Proxies a PC controller into the platform object
class PCControllerProxy(object):

    __metaclass__ = ProvidenceClarityController
    c_class = None

    def __init__(self, controller):
        if isinstance(controller, ProvidenceClarityController):
            self.c_class = controller
    
    def __get__(self, instance, owner):
        pass
        
    def __set__(self, instance, value):
        raise NotImplemented('Platform controller properties are read-only.')
        
    def __delete__(self, instance):
        raise NotImplemented('Platform controller properties are read-only.')
        

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
    
    ## ===== 2: Internals
    __log_map = logging._levelNames

    ## ===== 3: Internal Methods
    def __init__(self,config=False,**kwargs):
        
        if config is False:
            raise exceptions.ConfigRequired()
        else:
            self.config = config
            
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
        
        super(Platform, self).__init__()
        
    #def __repr__(self):
    #    return '<ProvidenceClarity '
    
    ## ===== 4: Class Methods
    @classmethod
    def config(cls):
        return cls.config

    @classmethod
    def version(cls):
        return cls.version
    

## Exception Master
class PCException(Exception):

    message = None

    def __init__(self, msg=None):
        self.message = msg
        
    
## Master Controller Object
class PCController(object):
    pass
    

# Log controller for logging
class PCLogController(PCController):
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