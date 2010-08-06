from . import StorageBackend


class WebStorageBackend(StorageBackend):
    
    @classmethod
    def store(cls, key, data):
        pass
    
    @classmethod
    def get(cls, key):
        pass