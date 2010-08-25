#
#   =====================================================
#   |==|  PROVIDENCE/CLARITY DATA ANALYSIS PLATFORM  |==|
#   |==|     -----------------------------------     |==|
#   |==| Author: Sam Gammon <sg@samgammon.com>       |==|
#   |==| Version: 0.1 DEV                          |==|
#   |==| ------------------------------------------- |==|
#   |==|   COPYRIGHT (c) 2010. ALL RIGHTS RESERVED   |==|
#   =====================================================
#

import os, sys, logging, exceptions


## Import Details
__all__ = ['api','data','services','main']
__protos__ = ['data']

## Declare Globals
version_major = 0.1
version_minor = 6.0
config_module = None
build = 'DEV'

## Expose Import-able Variables
VERSION = str(version_major)+'.'+str(version_minor)+' '+str(build)
PC_PATH = os.path.join(os.path.dirname(__file__))

## Init and return a ProvidenceClarity object
def initialize(namespace=None,config='pc_config'):

    # === 0: Grab Globals
    global version_major
    global version_minor
    global config_module
    global build

    # === 1: Path Inserts
    if '.' not in sys.path:
        sys.path.insert(0,'.')
        sys.path.insert(1,'lib')

    # === 2: Load Config
    try: config_mod = __import__(config,globals(),locals(),['get','dump','config'],-1);
    except ImportError: raise exceptions.InvalidConfig()

    # === 3: Import Masterclass    
    from main import ProvidenceClarity
    
    # === 4: Environment Vars
    software_t = '/'.split(os.environ['SERVER_SOFTWARE'])
    if software_t[0].lower() == 'development': platform = 'Dev';
    else: platform = 'Production'
    
    domain = os.environ['HTTP_HOST'].split(':')[0].split('.')
    if domain[-1] == 'com':
        subdomain = domain[0]
    else:
        subdomain = None

    if namespace is not None:
        _ns = subdomain
    else:
        _ns = namespace

    # === 5: Create the Object
    p = ProvidenceClarity(config_mod,namespace=_ns,version={'major':version_major,'minor':version_minor,'full':str(version_major)+'.'+str(version_minor)+' '+str(build),'build':build})
    
    
    return p