import exceptions
from ProvidenceClarity import PCController, PCAdapter, pc_config
from ProvidenceClarity.data.data import ORIGIN_LIST, FORMAT_LIST, DataStub, DataBackend
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.api.util import import_helper

adapters = pc_config.get('adapters','api.storage',[])



class StorageController(PCController):

    @classmethod
    def loadAdapter(cls,name):

        global adapters
        
        if backend in adapters:
            adapter = import_helper(adapters[backend])
        
            if adapter == False:
                raise exceptions.InvalidBackend()
                
            else:
                ### STOPPED HERE
                pass
                
    @classmethod
    def loadStubClass(cls,adapter):
        
        if isinstance(adapter, (str,basestring,unicode)):
            _adapter = DataBackend.get_by_key_name(adapter)

        elif isinstance(adapter, DataBackend):
            _adapter = adapter
            
        else:
            raise exceptions.InvalidBackend()
            
        stub_class = import_helper(adapter.model_path)
        if stub_class == False:
            return False
            
        else:
            return stub_class
        

class StorageAdapter(PCAdapter):

    @classmethod
    def store(cls, key, data):
        raise NotImplemented()


    @classmethod
    def generateStub(cls, key, data):
        raise NotImplemented()
        
    @classmethod
    def get(cls, key):
        raise NotImplemented()
        
        
class StubController(object):
    
    @classmethod
    def create(cls, origin, backend, format, **kwargs):
        
        b = StorageController.loadStubClass(backend)
        
        if isinstance(FORMAT_LIST.index(format), int):
            d.format = format
            d.format_other = None
        else:
            d.format = 'other'
            d.format_other = format            
            
        if isinstance(ORIGIN_LIST.index(source), int):
            d.origin = origin
            d.origin_other = None
        else:
            d.origin = 'other'
            d.origin_other = origin
            
        return d.put()
    
    
    @classmethod
    def store(self, stub, data=None):
        
        from blobstore import BlobstoreBackend
        from webstorage import WebStorageBackend
        
        if isinstance(stub, BlobstoreData):
            stub.data_ref = BlobstoreBackend.store(stub, data)
            
        elif isinstance(stub, WebStorageData):
            stub.data_ref = WebStorageBackend.store(stub, data)
            
        return stub.put()
        
        
    @classmethod
    def getAndValidate(cls, **kwargs):
        pass