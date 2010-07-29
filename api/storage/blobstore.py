from . import StorageBackend


class BlobstoreBackend(StorageBackend):
    
    @classmethod
    def store_data(cls, key, data):
        pass
    
    @classmethod
    def get_data(cls, key):
        pass