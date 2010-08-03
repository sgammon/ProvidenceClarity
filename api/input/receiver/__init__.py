from .. import InputAdapter

import exceptions
from ProvidenceClarity.data.input import DataReceiver


class ReceiverController(InputAdapter):

    model = None        

    ## Retrieve receiver for use
    @classmethod
    def getAndValidate(cls, request, for_use=True):
        
        path_t = request.path.split('/')
        
        d = DataReceiver.get_by_key_name('.'.join(path_t[path_t.index('receiver'):len(path_t))]))
        
        if d is not None:
            
            if d.enabled != True:
                raise exceptions.ReceiverDisabled()
            else:
                self.model = d
                if for_use: return d; else return True
        else:
            raise exceptions.ReceiverNotFound()
            
    ## Create a new receiver
    @classmethod
    def new(cls, name, data_handler, data_type, storage_backend='blobstore', enable=False, **kwargs):
        
        if isinstance(name, list):
            name = '.'.join(name)
            
        return DataReceiver(key_name=name,data_handler=data_handler,storage_backend=storage_backend,enabled=enable,**kwargs).put()
    
    ## Store data after being processed
    @classmethod
    def store(cls, data, receiver):
        
        pass