from . import StorageBackend


class BlobstoreBackend(StorageBackend):
    
    @classmethod
    def store(cls, key, data):
        pass
    
    @classmethod
    def get(cls, key):
        pass