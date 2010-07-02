import logging, sys
from . import DataManager

from ProvidenceClarity.data.proto import P

class ProtoController(object):

    @classmethod
    def import_helper(cls, module, fromlist=['*']):
        
        try:
            helper = __import__(module,globals(),locals(),fromlist)
            return helper

        except ImportError:
            #@TODO: Find a way to store errors in datastore
            logging.info('[i]: Error importing module '+str(module)+' with fromlist '+str(fromlist))
            return False
            
    @classmethod
    def _perform_inserts(cls, module):
        
        helper = cls.import_helper(module)
        
        if helper is not False and hasattr(helper, 'ProtoHelper'):
            helper = helper.ProtoHelper()
        else:
            return False

        return helper.do_insert()
        
    @classmethod
    def _perform_clean(cls, module):
        
        helper = cls.import_helper(module)

        if helper is not False and hasattr(helper, 'ProtoHelper'):
            helper = helper.ProtoHelper()
        else:
            return False

        return helper.do_clean()
    
    @classmethod
    def _valid_module(cls, module):
        """ Proto operations that accept a module as a parameter only accept type:str and type:module. """
        
        if isinstance(module, (basestring, type(sys))):
            return True
        else:
            return False
    
    @classmethod
    def _recursive_action(cls, module, action):

        if cls._valid_module(module):

            if isinstance(module, basestring):
                module = cls.import_helper(module)

            ## start with the top-level import
            if hasattr(module, 'ProtoHelper'):
                
                h = module.ProtoHelper()
                                
                if hasattr(h, action):
                    #@TODO: Find out what to do with these results?
                    res = getattr(h, action)()
                    
                else:
                    pass
            
            ## proceed to submodule processing (use protos pointer if it exists)
            if hasattr(module, '__protos__'):
                
                for proto in getattr(module, '__protos__'):

                    submod_i = cls.import_helper(module.__name__, [proto])

                    if hasattr(module, proto):
                        submod = getattr(module, proto)

                        if submod != False:
                            cls._recursive_action(submod, action)
                    
        else:
            return False
        
        return True
    
    @classmethod
    def perform_inserts(cls, module, recursive=False):
        
        if recursive is False:
            return cls._perform_inserts(module)
            
        else:
            return cls._recursive_action(cls.import_helper(module), 'do_insert')
                    
    @classmethod
    def perform_clean(cls, module, recursive=False):
        
        if recursive is False:
            return cls._perform_clean(module)
            
        else:
            return cls._recursive_action(module, 'do_clean')