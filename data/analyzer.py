from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.input import DataInput
from ProvidenceClarity.data.mapreduce import MapperParam
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.expando import Expando
from ProvidenceClarity.data.core.polymodel import PolyModel


class AnalyzerEngine(Model, CreatedModifiedMixin):
    
    """ Abstract ancestor class describing a data processing engine that can be used by the Analyzer module. """
    
    handler_path = db.StringProperty()
    
    
class AnalyzerTemplate(Model, CreatedModifiedMixin):
    
    """ Represents a template of settings to be used for an analyzer job. """
    
    pass
    

class DataJob(PolyModel, CreatedModifiedMixin):

    """ Abstract ancestor class describing a data processing job. """
    
    status = db.StringProperty(choices=['queued','paused','processing','error','complete'])
    in_data = db.ReferenceProperty(DataInput, collection_name="jobs")
    out_storage = db.StringProperty(choices=['datastore','blobstore','bigstorage'])
    
    ## Job Progress
    analyzer_process = db.ListProperty(db.Key)
    current_analyzer = db.ReferenceProperty(AnalyzerEngine, collection_name="current_jobs")
    
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
    
    
class MapReduceJobParam(Expando):
    
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
                                    direct_parent=db.Key.from_path('P','DataJob'),ancestry_path=['DataJob'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=MapReduceJobParam,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Name for param.',keyid_use=None,keyparent_use='Job that owns param and value.'))
                                   
        self.models.append(self.P(_class=DirectStorageJob,
                                    direct_parent=db.Key.from_path('P','DataJob'),ancestry_path=['DataJob'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models

    def base(self):
        
        self.models.append(AnalyzerEngine(key_name='object',
                            handler_path='ProvidenceClarity.api.analyzer.object'))
                            
        self.models.append(AnalyzerEngine(key_name='relation',
                            handler_path='ProvidenceClarity.api.analyzer.relation'))
                            
        self.models.append(AnalyzerEngine(key_name='stat',
                            handler_path='ProvidenceClarity.api.analyzer.stat'))
        

        return self.models


    def clean(self):
        
        self.models.append(self.P.get_by_key_name('DataJob'))
        self.models.append(self.P.get_by_key_name('MapReduceJob'))
        self.models.append(self.P.get_by_key_name('MapReduceJobParam'))
        self.models.append(self.P.get_by_key_name('DirectStorageJob'))
        
        return self.models