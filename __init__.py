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

import os, sys, logging, exceptions
from google.appengine.api import namespace_manager, capabilities

import core
from ProvidenceClarity.core import api as c_api
from ProvidenceClarity.core import bridge as c_bridge
from ProvidenceClarity.core import clock as c_clock
from ProvidenceClarity.core import config as c_config
from ProvidenceClarity.core import controller as c_controller
from ProvidenceClarity.core import ext as c_ext
from ProvidenceClarity.core import log as c_log
from ProvidenceClarity.core import state as c_state

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
        

    
# Providence Clarity Platform!
class Platform(core.ProvidenceClarityObject):

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
    config      = c_config.PCConfigProxy
    log         = c_log.PCLogProxy
    clock       = c_clock.PCClockProxy
    state       = c_state.PCStateProxy
    api         = c_api.PCAPIProxy
    ext         = c_ext.PCExtProxy
    
    ## ===== 2: Internals
    __log_map = logging._levelNames

    ## ===== 3: Internal Methods
    def __init__(self,config_override=None, *args, **kwargs):
        
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
        self.config = c_config.PCConfigProxy()
        self.log = c_log.PCLogProxy()
        self.clock = c_clock.PCClockProxy()        
        self.state = c_state.PCStateProxy()
        self.api = c_api.PCAPIProxy()
        self.ext = c_ext.PCExtProxy()
        
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
                                        
        ## Load/resolve Config
        if config_override is None:
            config_mod, props = import_helper(['ProvidenceClarity','pc_config'],['get','dump','config'])
            
        elif config_override is False or config_override == '':
            raise exceptions.ConfigRequired()

        else:

            if isinstance(config_override, type(os)):
                config_mod = config_override

            elif isinstance(config_override, (str, basestring, unicode)):
                config_mod, props = import_helper(config_override,['get','dump','config'])

            elif isinstance(config_override, list):
                config_mod, props = import_helper('.'.join(config_override))
                
            else:
                try:
                    config_mod, props = import_helper(['ProvidenceClarity',config_override],['get','dump','config'])
            
                except ImportError: raise exceptions.InvalidConfig()
                
        ## Set configuration
        self.config.setConfig(config_mod)
          
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
PCController = c_controller.PCController


## Master Adapter Object
PCAdapter = c_controller.PCAdapter            
        

## Init and return a ProvidenceClarity object
def initialize(platform_profile=None,namespace=None,config='pc_config'):

    if platform_profile is not None:
        if isinstance(platform_profile, ProvidenceClarityPlatform):
            p = platform_profile(namespace=namespace,config=config)
    else:
        p = Platform(config)
    return p