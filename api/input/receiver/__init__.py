from .. import InputAdapter, InputController

import exceptions
from ProvidenceClarity.data.input import DataReceiver
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.api.storage import StubController

class ReceiverController(InputAdapter, InputController):

    model = None        

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
                if for_use:
                    return d
                else: return True
        else:
            raise exceptions.ReceiverNotFound()
            
    
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
        

class ReceiverHandler(object):
    
    """ Receiver extensions external to P/C extend this. """

    data = None # Raw Data
    p_data = None # Processed Data


    def process_data(self, data):

        """ Default prototype method returns inputted data. """

        return data