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

import os
import logging

class ProvidenceClarity(object):

    ## ===== 1: Properties (Initialized Externally)
    version     = None
    config      = None
    config_path = None
    
    ## ===== 2: Internals
    __log_map = logging._levelNames

    ## ===== 3: Methods
    @classmethod
    def config(cls):
        return cls.config

    @classmethod
    def version(cls):
        return cls.version
    
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
        