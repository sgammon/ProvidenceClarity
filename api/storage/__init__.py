from .. import AdapterInterface
from ProvidenceClarity import PCController
from ProvidenceClarity.data.data import ORIGIN_LIST, FORMAT_LIST, DataStub, BlobstoreData, WebStorageData


class StorageController(PCController):
    pass

class StorageAdapter(AdapterInterface):

    stub = None

    @classmethod
    def store(cls, key, data):
        pass
        
    @classmethod
    def get(cls, key):
        pass
        
        
class StubController(object):
    
    @classmethod
    def create(cls, origin, backend, format, **kwargs):
        
        from blobstore import BlobstoreBackend
        from webstorage import WebStorageBackend

        if backend == 'blobstore':
            d = BlobstoreData(**kwargs)
            
        elif backend == 'webstorage':
            d = WebStorageData(**kwargs)
            
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