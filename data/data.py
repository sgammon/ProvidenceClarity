from ProvidenceClarity.api.data import DataManager
from google.appengine.ext import blobstore, db
from ProvidenceClarity import pc_config
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.proto import P
from ProvidenceClarity.data.input import DataInput
from ProvidenceClarity.data.services import ServiceAdapter
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.expando import Expando
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


class DataBackend(ServiceAdapter):
    
    """ Describes a facility for P/C to store data. """
    
    # key_name = Name of backend
    file_size_limit = db.IntegerProperty()
    model_class = db.ReferenceProperty(P, collection_name='_data_backend')
    model_class_path = db.StringProperty()
    

class DataStub(PolyModel, CreatedModifiedMixin):
    
    """ Describes a piece of data stored externally from the GAE datastore. """
    
    backend = db.ReferenceProperty(DataBackend, collection_name='stubs')
    source = db.ReferenceProperty(DataInput, collection_name='stubs', default=None)
    
    format = db.StringProperty(choices=FORMAT_LIST)
    format_other = db.StringProperty()
    
    origin = db.StringProperty(choices=ORIGIN_LIST)
    origin_other = db.StringProperty()
    
    ## Expiration
    expiration = db.DateTimeProperty()
    mark_for_delete = db.BooleanProperty()
    

class DatastoreData(DataStub):
    
    """ Represents a set of keys stored in the data store as a group. """
    
    BACKEND = 'datastore'
    data_ref = db.ListProperty(db.Key)
    

class BlobstoreData(DataStub):
    
    """ Represents data stored in the blobstore. """
    
    BACKEND = 'blobstore'
    data_ref = blobstore.BlobReferenceProperty()
    
    
class WebStorageData(DataStub):
    
    """ Represents data stored in Google Storage for Developers. """
     
    BACKEND = 'webstorage'
    data_ref = db.LinkProperty()


class StoredImage(BlobstoreData):
    
    """ Dynamic image stored and served by the datastore. """
    
    # Height/Format Properties
    width = db.IntegerProperty()
    height = db.IntegerProperty()
    img_format = db.StringProperty(choices=['jpeg','png','gif','bmp','tiff','ico'])
    
    # Image Permutations
    original = db.SelfReferenceProperty(collection_name='permutations')
    
    
class DataJob(PolyModel, CreatedModifiedMixin):

    """ Abstract ancestor class describing a data processing job. """
    
    status = db.StringProperty(choices=['prequeued','queued','paused','processing','error','complete'])
    in_data = db.ReferenceProperty(DataStub, collection_name="in_jobs")
    out_data = db.ReferenceProperty(DataStub, collection_name="out_jobs")
    out_storage = db.StringProperty(choices=['datastore','blobstore','bigstorage'])
    
    ## Job Progress
    current_step = db.StringProperty() ## key of DataJobEntry
        
    ## Scheduling
    do_after = db.DateTimeProperty()
    do_on = db.DateTimeProperty()
    
    ## Audit Trail
    queued_stamp = db.DateTimeProperty()
    error_stamp = db.DateTimeProperty()
    processing_stamp = db.DateTimeProperty()
    completed_stamp = db.DateTimeProperty() 
    
    
class DataJobEntry(PolyModel, CreatedModifiedMixin):
    
    """ A component of a datajob. """
    
    status = db.StringProperty(choices=['queued','paused','processing','error','complete'])    
    job = db.ReferenceProperty(DataJob, collection_name='job_entries')
    in_data = db.ReferenceProperty(DataStub, collection_name="in_job_entries")
    out_data = db.ReferenceProperty(DataStub, collection_name="out_job_entries")
    
    
class DataJobTemplate(Expando):
    
    """ Template for a set of arguments for a DataJob. """
    
    name = db.StringProperty()
    arguments = db.ListProperty(db.Key)
    

class#### HERE    

    
class DataJobTemplateEntry(PolyModel, CreatedModifiedMixin):
    
    """ A component of a datajobtemplate. """
    
    pass
    
    
class DataJobEntryArgument(Expando):
    
    """ Describes an argument to a DataJobEntry. """
    
    # key_name = key of key=>value
    entry = db.ReferenceProperty(DataJobEntry, collection_name='arguments')
    

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
                                   
        self.models.append(self.P(_class=DataBackend,
                                    direct_parent=db.Key.from_path('P','ServiceAdapter'),ancestry_path=['ServiceAdapter'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique name of storage backend.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataStub,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=BlobstoreData,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=WebStorageData,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DatastoreData,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=StoredImage,
                                    direct_parent=db.Key.from_path('P','DataStub'),ancestry_path=['DataStub'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        self.models.append(self.P(_class=DataJob,
                             direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                             created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    
    def base(self):
        
        self.models.append(TaskQueue(key_name='default',name='Default',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='outgoing-mail',name='Outgoing: Mail',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='outgoing-xmpp',name='Outgoing: XMPP',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='input-fetcher',name='Input: Fetch',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='object-analyzer',name='Analyzer: Object',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='relation-analyzer',name='Analyzer: Relation',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='graph-analyzer',name='Analyzer: Stat',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='mapreduce-analyzer',name='Analyzer: MapReduce',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='transaction-queue',name='Data: Transaction Controller',status='activated'))                                                                
        self.models.append(TaskQueue(key_name='cacher',name='Data: Cache Controller',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='indexer',name='Data: Index Controller',status='activated'))                                                        
        self.models.append(TaskQueue(key_name='data-hygiene',name='Data: Hygiene Controller',status='activated'))
        
        self.models.append(DataBackend(key_name='datastore',name='BigTable Datastore Driver',
                                        model_class=self.P.get_by_key_name('DatastoreData'),
                                        model_class_path='ProvidenceClarity.data.data.DatastoreData'))
                                        
        self.models.append(DataBackend(key_name='blobstore',name='Blobstore Driver',
                                        model_class=self.P.get_by_key_name('BlobstoreData'),
                                        model_class_path='ProvidenceClarity.data.data.BlobstoreData'))
                                        
        self.models.append(DataBackend(key_name='datastore',name='Storage for Developers Driver',
                                        model_class=self.P.get_by_key_name('WebStorageData'),
                                        model_class_path='ProvidenceClarity.data.data.WebStorageData'))

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
        self.models.append(self.P.get_by_key_name('DataBackend'))
        self.models.append(self.P.get_by_key_name('DatastoreData'))
        self.models.append(self.P.get_by_key_name('BlobstoreData'))
        self.models.append(self.P.get_by_key_name('WebStorageData'))
        self.models.append(self.P.get_by_key_name('S3Data'))
        self.models.append(self.P.get_by_key_name('StoredImage'))
        
        return self.models