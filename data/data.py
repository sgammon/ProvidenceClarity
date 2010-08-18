from ProvidenceClarity.api.data import DataManager
from google.appengine.ext import blobstore, db
from ProvidenceClarity import pc_config
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util


FORMAT_LIST = ['json','xml','text','blob','other']
ORIGIN_LIST = ['input','analyzer','cache','other']

_CACHE_ENTITIES_ON_CREATE = pc_config.get('cache_on_create','data.entity.E',False)
_INDEX_ENTITIES_ON_CREATE = pc_config.get('cache_on_create','data.entity.E',True)


class TaskQueue(Model):
    name = db.StringProperty()
    status = db.StringProperty(choices=['activated','paused'])


class QueuedTask(PolyModel, CreatedModifiedMixin):
    queue = db.ReferenceProperty(TaskQueue, collection_name='tasks')
    status = db.StringProperty(choices=['processing','queued','standby','complete'],default='queued')
    eta = db.DateTimeProperty(default=None, indexed=False)
    work_start = db.DateTimeProperty(indexed=False)
    work_end = db.DateTimeProperty(indexed=False)
    chain_length = db.IntegerProperty(indexed=False)
    success = db.BooleanProperty(default=False)
    next_task = db.SelfReferenceProperty(collection_name='previous_task')
    
    
class QueuedTransaction(QueuedTask):
    retries = db.IntegerProperty()
    

class WriteOperation(QueuedTransaction):
    subject = util.CachedProtobuf()
    #attachments = util.CachedProtobufList() #@TODO: Find out why this is always marked 'required'
    
    
class DeleteOperation(QueuedTransaction):
    subject  = db.ListProperty(db.Key)
    scrub_decorators = db.BooleanProperty(default=True)
    scrub_indexes = db.BooleanProperty(default=True)
    scrub_cache = db.BooleanProperty(default=True)
    scrub_children = db.BooleanProperty(default=True)
    

class EntityCreateTask(WriteOperation):
    queue_indexing = db.BooleanProperty(default=_INDEX_ENTITIES_ON_CREATE)
    queue_caching = db.BooleanProperty(default=_CACHE_ENTITIES_ON_CREATE)
    
    
class EntityUpdateTask(WriteOperation):
    pass
    

class EntityDeleteTask(DeleteOperation):
    pass


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