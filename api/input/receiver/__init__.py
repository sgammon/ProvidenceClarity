from .. import InputAdapter, InputController

import exceptions
from ProvidenceClarity.data.input import DataReceiver
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.api.util import import_helper
from ProvidenceClarity.api.storage import StubController

class ReceiverController(InputController):

    model = None
    handler = None    

    ## Retrieve receiver for use
    @classmethod
    def getAndValidate(cls, request, for_use=True):
        
        path_t = request.path.split('/')
        
        d = DataReceiver.get_by_key_name('.'.join(path_t[path_t.index('receiver'):len(path_t)]))
        
        if d is not None:
            
            if d.enabled != True:
                raise exceptions.ReceiverDisabled()
            else:
                self.model = d
                if d.data_handler is not None:
                    
                    data_handler = None
                    mod, prop = import_helper(d.data_handler[0:-1],d.data_handler[-1])
                    
                    if issubclass(prop, DataReceiver):
                        data_handler = prop[d.data_handler[-1]]
                    else:
                        raise exceptions.InvalidDataHandler()
                    
                if for_use:
                    return (d, data_handler)
                else: return True
        else:
            raise exceptions.ReceiverNotFound()
            
            
    @classmethod
    def loadAdapter(cls, path):
        
        pass
            
    
    ## Create a new receiver
    @classmethod
    def create(cls, name, data_handler, data_type, storage_backend='blobstore', enable=False, **kwargs):
        
        if isinstance(name, list):
            name = '.'.join(name)
            
        if isinstance(data_handler, object):
            handler_i = data_module.__module__.split('.')
            
        elif isinstance(data_handler, str):
            handler_i = data_handler
            
        return DataReceiver(key_name=name,data_type=data_type,data_handler=handler_i,storage_backend=storage_backend,enabled=enable,**kwargs).put()
    
    
    ## Store data after being processed
    @classmethod
    def get_stub(cls, data, receiver):
        
        return StubController.create('receiver',r.storage_backend,r.format)
        
        
class ReceiverAdapter(InputAdapter):
    
    """ Receiver extensions external to P/C extend this. """

    data = None # Raw Data
    p_data = None # Processed Data


    def adapt(self, input):
        return self.process_data(input)

    def process_data(self, data):

        """ Default prototype method returns inputted data. """

        return data