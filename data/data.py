from ProvidenceClarity.api.data import DataManager
from google.appengine.ext import blobstore, db
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.polymodel import PolyModel


FORMAT_LIST = ['json','xml','text','blob','other']
ORIGIN_LIST = ['input','analyzer','cache','other']

class DataEntry(PolyModel, CreatedModifiedMixin): """ Describes an entry in a feed of data to be consumed by the system. """


class DataStub(PolyModel, CreatedModifiedMixin):
    
    """ Describes a piece of data stored externally from the GAE datastore. """
    
    format = db.StringProperty(choices=FORMAT_LIST)
    format_other = db.StringProperty()
    
    origin = db.StringProperty(choices=ORIGIN_LIST)
    origin_other = db.StringProperty()
    
    ## Expiration
    expiration = db.DateTimeProperty()
    mark_for_delete = db.BooleanProperty()
    

class BlobstoreData(DataStub):
    
    BACKEND = 'blobstore'
    
    data_ref = blobstore.BlobReferenceProperty()
    
    
class WebStorageData(DataStub):
    
    BACKEND = 'webstorage'
    
    data_ref = db.LinkProperty()


class StoredImage(DataStub):
    
    """ Dynamic image stored and served by the datastore. """
    
    # Height/Format Properties
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    img_format = db.StringProperty(choices=['jpeg','png','gif','bmp','tiff','ico'])
    
    # Image Permutations
    original = db.SelfReferenceProperty(collection_name='permutations')
    

## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=DataEntry,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataStub,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=BlobstoreData,
                                    direct_parent=db.Key.from_path('Proto','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=WebStorageData,
                                    direct_parent=db.Key.from_path('Proto','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=StoredImage,
                                    direct_parent=db.Key.from_path('Proto','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('DataEntry'))
        self.models.append(self.P.get_by_key_name('DataStub'))
        self.models.append(self.P.get_by_key_name('BlobstoreData'))
        self.models.append(self.P.get_by_key_name('WebStorageData'))
        self.models.append(self.P.get_by_key_name('StoredImage'))
        
        return self.models