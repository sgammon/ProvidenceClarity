#
#   =====================================================
#   |==|  PROVIDENCE/CLARITY DATA ANALYSIS PLATFORM  |==|
#   |==|     -----------------------------------     |==|
#   |==| Author: Sam Gammon <sg@samgammon.com>       |==|
#   |==| Version: 0.5 ALPHA                          |==|
#   |==| ------------------------------------------- |==|
#   |==|   COPYRIGHT (c) 2010. ALL RIGHTS RESERVED   |==|
#   =====================================================
#

import os, sys

## Import Details
__all__ = ['api','data','services','main']

## Declare Globals
version_major = 0.5
version_minor = 1.31
config_module = None
build = 'DEV'

## Init and return a ProvidenceClarity object
def initialize(config='pc_config_default'):

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
    try: config_mod = __import__(config,globals(),locals(),[],-1);
    except ImportError: exit() # @TODO: Implement error/exception here

    # === 3: Import Masterclass    
    from main import *
    
    # === 4: Environment Vars
    software_t = '/'.split(os.environ['SERVER_SOFTWARE'])
    if software_t[0].lower() == 'development': platform = 'Dev';
    else: platform = 'Production'

    # === 5: Create the Object
    p = ProvidenceClarity()
    
    # === 6: Assign Properties
    p.version_major = version_major
    p.version_minor = version_minor
    p.version = str(version_major)+'.'+str(version_minor)+' '+str(build)
    p.build = build
    p.config_path = config
    p.config = config_mod
    config_module = config_mod
    
    return p