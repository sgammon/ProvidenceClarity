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
_INDEX_ENTITIES_ON_CREATE = pc_config.get('index_on_create','data.entity.E',True)


class TaskQueue(Model):

    """ Represents a AppEngine task queue that is used by ProvidenceClarity. """

    name = db.StringProperty()
    status = db.StringProperty(choices=['activated','paused'])
    last_use = db.DateTimeProperty()


class QueuedTask(PolyModel, CreatedModifiedMixin):
    
    """ Represents a ticket for a queued task waiting/being executed by a TaskQueue. """
    
    queue = db.ReferenceProperty(TaskQueue, collection_name='tasks')
    status = db.StringProperty(choices=['processing','queued','standby','complete'],default='queued')
    eta = db.DateTimeProperty(default=None, indexed=False)
    work_start = db.DateTimeProperty(indexed=False)
    work_end = db.DateTimeProperty(indexed=False)
    chain_length = db.IntegerProperty(indexed=False,default=1)
    success = db.BooleanProperty(default=False)
    next_task = db.SelfReferenceProperty(collection_name='previous_task')
    
    
class QueuedTransaction(QueuedTask):
    
    """ Represents a data transaction that has been queued for commit to the datastore (or queued for delete). """
    
    retries = db.IntegerProperty(default=3)
    

class WriteOperation(QueuedTransaction):
    
    """ A QueuedTransaction that intends to write new data to the datastore. """
    
    subject = util.CachedProtobuf()
    #attachments = util.CachedProtobufList() #@TODO: Find out why this is always marked 'required'
    
    
class DeleteOperation(QueuedTransaction):
    
    """ A QueuedTransaction that intends to delete data from the datastore. """
    
    subject  = db.ListProperty(db.Key)
    scrub_decorators = db.BooleanProperty(default=True)
    scrub_indexes = db.BooleanProperty(default=True)
    scrub_cache = db.BooleanProperty(default=True)
    scrub_children = db.BooleanProperty(default=True)
    

class EntityCreateTask(WriteOperation):
    
    """ A WriteOperation for creating new entities along with descriptors and proper inheritance structure. """
    
    queue_indexing = db.BooleanProperty(default=_INDEX_ENTITIES_ON_CREATE)
    queue_caching = db.BooleanProperty(default=_CACHE_ENTITIES_ON_CREATE)
    
    
class EntityUpdateTask(WriteOperation):
    
    """ A WriteOperation for queue-ing and executing an update to an entity. """
    
    pass
    

class EntityDeleteTask(DeleteOperation):
    
    """ A DeleteOperation for removing an entity and its associated ancestry structure. """
    
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
        
        self.models.append(self.P(_class=TaskQueue,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=False,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Official system name of task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=QueuedTask,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=QueuedTransaction,
                                    direct_parent=db.Key.from_path('P','QueuedTask'),ancestry_path=['QueuedTask'],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=WriteOperation,
                                    direct_parent=db.Key.from_path('P','QueuedTransaction'),ancestry_path=['QueuedTask','QueuedTransaction'],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DeleteOperation,
                                    direct_parent=db.Key.from_path('P','QueuedTransaction'),ancestry_path=['QueuedTask','QueuedTransaction'],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=EntityCreateTask,
                                    direct_parent=db.Key.from_path('P','WriteOperation'),ancestry_path=['QueuedTask','QueuedTransaction','WriteOperation'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=EntityUpdateTask,
                                    direct_parent=db.Key.from_path('P','WriteOperation'),ancestry_path=['QueuedTask','QueuedTransaction','WriteOperation'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=EntityDeleteTask,
                                    direct_parent=db.Key.from_path('P','DeleteOperation'),ancestry_path=['QueuedTask','QueuedTransaction','DeleteOperation'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Ticket URN for looking up the ticket from the task queue.',keyid_use=None,keyparent_use=None))
                
        self.models.append(self.P(_class=DataEntry,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataStub,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=BlobstoreData,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=WebStorageData,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=StoredImage,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    
    def base(self):
        
        self.models.append(TaskQueue(key_name='default',name='Default',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='outgoing-mail',name='Outgoing: Mail',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='outgoing-xmpp',name='Outgoing: XMPP',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='input-scraper',name='Input: Scraper',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='analyzer-object',name='Analyzer: Object',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='analyzer-relation',name='Analyzer: Relation',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='analyzer-stat',name='Analyzer: Stat',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='analyzer-mapreduce',name='Analyzer: MapReduce',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='transaction-queue',name='Data: Transaction Controller',status='activated'))                                                                
        self.models.append(TaskQueue(key_name='cacher',name='Data: Cache Controller',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='indexer',name='Data: Index Controller',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='data-hygiene',name='Data: Hygiene Controller',status='activated'))

        return self.models

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('TaskQueue'))
        self.models.append(self.P.get_by_key_name('QueuedTask'))
        self.models.append(self.P.get_by_key_name('QueuedTransaction'))
        self.models.append(self.P.get_by_key_name('WriteOperation'))
        self.models.append(self.P.get_by_key_name('DeleteOperation'))
        self.models.append(self.P.get_by_key_name('EntityCreateTask'))
        self.models.append(self.P.get_by_key_name('EntityUpdateTask'))
        self.models.append(self.P.get_by_key_name('EntityDeleteTask'))
        self.models.append(self.P.get_by_key_name('NormalizedObject'))
        self.models.append(self.P.get_by_key_name('DataEntry'))
        self.models.append(self.P.get_by_key_name('DataStub'))
        self.models.append(self.P.get_by_key_name('BlobstoreData'))
        self.models.append(self.P.get_by_key_name('WebStorageData'))
        self.models.append(self.P.get_by_key_name('StoredImage'))
        
        return self.models