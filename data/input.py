from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager, DataBackend
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.polymodel import PolyModel


class DataInput(PolyModel, CreatedModifiedMixin):
    
    """ Abstract ancestor class for data input classes (receivers and fetchers). """
    
    description = db.TextProperty()
    enabled = db.BooleanProperty(default=True)
    format = db.StringProperty(choices=['xml','json','html','text','rdf','binary'])
    storage_backend = db.StringProperty(choices=['datastore','blobstore','bigstorage'])
    

class DataReceiver(DataInput, CreatedModifiedMixin):
    
    """ Represents an endpoint for receiving data sent to P/C. """
    
    default_format = db.StringProperty()
    default_storage_backend = db.ReferenceProperty(DataBackend, collection_name='receivers', required=True)
    default_job_template = db.ReferenceProperty(DataJobTemplate, required=True)
    
    
class DataFetcher(DataInput, CreatedModifiedMixin): """ Describes a data fetcher. Usually runs on a cron. """
class DataSource(DataInput, CreatedModifiedMixin): """ Describes a source of data to be consumed by the system. """
class DataFeed(DataInput, CreatedModifiedMixin): """ Describes a feed of data to be consumed by the system. """


## Proto Inserts

class ProtoHelper(DataManager):

    models = []

    def insert(self):
        
        self.models.append(self.P(_class=DataInput,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataReceiver,
                                    direct_parent=db.Key.from_path('P','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique receiver name (used in receiver URL).',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataFetcher,
                                    direct_parent=db.Key.from_path('P','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique fetcher name (used in fetcher URL).',keyid_use=None,keyparent_use=None))
        
        self.models.append(self.P(_class=DataSource,
                                    direct_parent=db.Key.from_path('P','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True))
                                   
        self.models.append(self.P(_class=DataFeed,
                                    direct_parent=db.Key.from_path('P','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('DataInput'))
        self.models.append(self.P.get_by_key_name('DataReceiver'))
        self.models.append(self.P.get_by_key_name('DataFetcher'))
        self.models.append(self.P.get_by_key_name('DataSource'))
        self.models.append(self.P.get_by_key_name('DataFeed'))
        
        return self.models