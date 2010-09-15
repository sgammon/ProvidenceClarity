from google.appengine.ext import blobstore
from ProvidenceClarity.api.storage import StorageAdapter


class BlobstoreAdapter(StorageAdapter):
    
    @classmethod
    def store(cls, key, data):

        pass
        
    
    @classmethod
    def get(cls, key):

        if isinstance(key, str):
            key = blobstore.BlobKey(key)
            
        
            
        