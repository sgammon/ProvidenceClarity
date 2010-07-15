from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.input import DataInput
from ProvidenceClarity.data.mapreduce import MapperParam
from ProvidenceClarity.data.core.polymodel import PolyModel


class DataJob(PolyModel, CreatedModifiedMixin):

    """ Abstract ancestor class describing a data processing job. """
    
    status = db.StringProperty(choices=['queued','paused','processing','error','complete'])
    in_data = db.ReferenceProperty(DataInput, collection_name="jobs")
    out_storage = db.StringProperty(choices=['datastore','blobstore','bigstorage'])
    
    ## Status Flags
    complete = db.BooleanProperty()
    queued = db.BooleanProperty()
    error = db.BooleanProperty()
    processing = db.BooleanProperty()
    
    ## Scheduling
    do_after = db.DateTimeProperty()
    do_on = db.DateTimeProperty()
    
    ## Audit Trail
    queued_stamp = db.DateTimeProperty()
    error_stamp = db.DateTimeProperty()
    processing_stamp = db.DateTimeProperty()
    completed_stamp = db.DateTimeProperty()
    
    
class MapReduceJob(DataJob):

    """ Describes a Map/Reduce data processing job. """
    
    mapper = db.StringProperty()
    
    
class MapReduceJobParam(db.Expando):
    
    """ Maps a param to a value for a map reduce job. """
    
    job = db.ReferenceProperty(MapReduceJob, collection_name="params")
    param = db.ReferenceProperty(MapperParam, collection_name="mapped_params")
    
    
class DirectStorageJob(DataJob):

    """ Describes a data processing job executed from a simple Python module. """
    
    python_mod = db.ListProperty(basestring)
    
    
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=DataJob,
                             direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                             created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                             
        self.models.append(self.P(_class=MapReduceJob,
                                    direct_parent=db.Key.from_path('Proto','DataJob'),ancestry_path=['DataJob'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=MapReduceJobParam,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Name for param.',keyid_use=None,keyparent_use='Job that owns param and value.'))
                                   
        self.models.append(self.P(_class=DirectStorageJob,
                                    direct_parent=db.Key.from_path('Proto','DataJob'),ancestry_path=['DataJob'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models


    def clean(self):
        
        self.models.append(self.P.get_by_key_name('DataJob'))
        self.models.append(self.P.get_by_key_name('MapReduceJob'))
        self.models.append(self.P.get_by_key_name('MapReduceJobParam'))
        self.models.append(self.P.get_by_key_name('DirectStorageJob'))
        
        return self.models