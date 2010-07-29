from . import StorageBackend


class WebStorageBackend(StorageBackend):
    
    @classmethod
    def store_data(cls, key, data):
        pass
    
    @classmethod
    def get_data(cls, key):
        pass