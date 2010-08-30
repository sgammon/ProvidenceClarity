from . import StorageAdapter


class WebStorageBackend(StorageAdapter):
    
    @classmethod
    def store(cls, key, data):
        pass
    
    @classmethod
    def get(cls, key):
        pass