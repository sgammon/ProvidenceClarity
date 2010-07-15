from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.polymodel import PolyModel

class DataInput(PolyModel, CreatedModifiedMixin):
    
    """ Abstract ancestor class for data input classes (receivers and scrapers). """
    
    description = db.TextProperty()
    inactive = db.BooleanProperty()
    data_type = db.StringProperty(choices=['xml','json','html','text','rdf','binary'])
    storage_backend = db.StringProperty(choices=['datastore','blobstore','bigstorage'])


class DataReceiver(DataInput, CreatedModifiedMixin): """ Represents an endpoint for receiving data sent to P/C. """
class DataScraper(DataInput, CreatedModifiedMixin): """ Describes a data scraper. Usually runs on a cron. """
class DataSource(DataInput, CreatedModifiedMixin): """ Describes a source of data to be consumed by the system. """
class DataFeed(DataInput, CreatedModifiedMixin): """ Describes a feed of data to be consumed by the system. """
class DataEntry(PolyModel, CreatedModifiedMixin): """ Describes an entry in a feed of data to be consumed by the system. """

## Proto Inserts

class ProtoHelper(DataManager):

    models = []

    def insert(self):
        
        self.models.append(self.P(_class=DataInput,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataReceiver,
                                    direct_parent=db.Key.from_path('Proto','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique receiver name (used in receiver URL).',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=DataScraper,
                                    direct_parent=db.Key.from_path('Proto','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique scraper name (used in scraper URL).',keyid_use=None,keyparent_use=None))
        
        self.models.append(self.P(_class=DataSource,
                                    direct_parent=db.Key.from_path('Proto','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True))
                                   
        self.models.append(self.P(_class=DataFeed,
                                    direct_parent=db.Key.from_path('Proto','DataInput'),ancestry_path=['DataInput'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True))
                                   
        self.models.append(self.P(_class=DataEntry,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('DataInput'))
        self.models.append(self.P.get_by_key_name('DataReceiver'))
        self.models.append(self.P.get_by_key_name('DataScraper'))
        self.models.append(self.P.get_by_key_name('DataSource'))
        self.models.append(self.P.get_by_key_name('DataFeed'))
        self.models.append(self.P.get_by_key_name('DataEntry'))
        
        return self.models    