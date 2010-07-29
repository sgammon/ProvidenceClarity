from google.appengine.db import blobstore
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.polymodel import PolyModel


class DataEntry(PolyModel, CreatedModifiedMixin): """ Describes an entry in a feed of data to be consumed by the system. """


class DataStub(PolyModel, CreatedModifiedMixin):
    
    """ Describes a piece of data stored externally from the GAE datastore. """
    
    format = db.StringProperty(choices=['json','xml','text','blob'])
    
    origin = db.StringProperty(choices=['input','analyzer','cache','other'])
    origin_other = db.StringProperty()
    
    ## Expiration
    expiration = db.DateTimeProperty()
    mark_for_delete = db.BooleanProperty()
    

class BlobstoreData(DataStub):
    
    BACKEND = 'blobstore'
    
    data = blobstore.BlobReferenceProperty()
    
    
class WebStorageData(DataStub):
    
    BACKEND = 'webstorage'
    
    url = db.LinkProperty()


class StoredImage(DataStub):
    
    """ Dynamic image stored and served by the datastore. """
    
    # Height/Format Properties
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    img_format = db.StringProperty(choices=['jpeg','png','gif','bmp','tiff','ico'])
    
    # Image Permutations
    original = db.SelfReferenceProperty(collection_name='permutations')