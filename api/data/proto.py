import logging, sys
from . import DataManager
from . import DataController

from ProvidenceClarity import pc_config

from ProvidenceClarity.data.proto import P

do_log = pc_config.get('log_imports','api.data.proto.ProtoController',False)

class ProtoController(object):
            
    @classmethod
    def import_helper(cls,name,fromlist=None):
        
        if do_log: logging.info("[i]: Import request: \'"+str(name)+"\' with fromlist \'"+str(fromlist)+"\'.")
        
        try:
            
            if fromlist is not None:
            
                _fromlist_i = []
            
                if isinstance(fromlist, str):
                    _fromlist_i[0] = fromlist
                    
                elif isinstance(fromlist, list):
                    _fromlist_i = fromlist
                    
                for subitem in fromlist:
                    submod = __import__(name+'.'+subitem)

            else:
                mod = __import__(name)
                if do_log: logging.info("[i]: === Import Statement: \""+name+'".')

            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
                if do_log: logging.info("[i]: ====== Traversing "+str(mod)+" for "+str(comp)+'.')
            
            if do_log: logging.info("[i]: === Returning "+str(mod)+'.')
            return mod
            
        except ImportError:
            if do_log: logging.info("[i]: === ImportError exception encountered: \""+str(name)+"\".")
            #TODO: Find a way to store errors in the datastore
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
    def _perform_base(cls, module):
        
        helper = cls.import_helper(module)
        
        if helper is not False and hasattr(helper, 'ProtoHelper'):
            helper = helper.ProtoHelper()
        else:
            return False

        return helper.do_base()
        
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

        if module == False:
            if do_log: logging.info('[i]: Recursive action got False module.')
            return None

        if do_log: logging.info('[i]: Recursive action on \''+str(module.__name__)+'\'.')

        if cls._valid_module(module):

            if isinstance(module, basestring):
                module = cls.import_helper(module,['ProtoController','__protos__'])

            ## start with the top-level import
            if hasattr(module, 'ProtoHelper'):
                
                if do_log: logging.info('[i]: ==== Found module-level ProtoHelper.')                
                
                h = module.ProtoHelper()
                                
                if hasattr(h, action):
                    #@TODO: Find out what to do with these results?
                    res = getattr(h, action)()
                    if do_log: logging.info('[i]: ======= Found requested action, running.')                    
                    
                else:
                    if do_log: logging.info('[i]: ======= Could not find requested action.')

    
            ## proceed to submodule processing (use protos pointer if it exists)
            if hasattr(module, '__protos__'):

                if do_log: logging.info('[i]: === Found __protos__ pointer...')

                for proto in getattr(module, '__protos__'):

                    submod_i = cls.import_helper(module.__name__+'.'+proto)
                    if do_log: logging.info('[i]: ====== Sub-import statement: \''+module.__name__+'.'+proto+'\'.')

                    if hasattr(module, proto):
                        
                        if do_log: logging.info('[i]: ======= Retrieved valid submodule \''+str(proto)+'\'.')
                        
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
    def perform_base(cls, module, recursive=False):
        
        if recursive is False:
            return cls._perform_base(module)
            
        else:
            return cls._recursive_action(cls.import_helper(module), 'do_base')
                    
    @classmethod
    def perform_clean(cls, module, recursive=False):
        
        if recursive is False:
            return cls._perform_clean(module)
            
        else:
            return cls._recursive_action(module, 'do_clean')