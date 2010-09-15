from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager, DataJob
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.data import DataStub, DataJobEntry
from ProvidenceClarity.data.mapreduce import MapperParam
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.expando import Expando
from ProvidenceClarity.data.core.polymodel import PolyModel


class AnalyzerEngine(Model, CreatedModifiedMixin):
    
    """ Abstract ancestor class describing a data processing engine that can be used by the Analyzer module. """
    
    handler_path = db.StringProperty()
    description = db.TextProperty()
    
    
class AnalyzerTemplate(Model, CreatedModifiedMixin):
    
    """ Represents a template of settings to be used for an analyzer job. """
    
    pass
    
    
class MapReduceJob(DataJobEntry):

    """ Describes a Map/Reduce data processing job. """
    
    mapper = db.StringProperty()
    
    
class MapReduceJobParam(Expando):
    
    """ Maps a param to a value for a map reduce job. """
    
    job = db.ReferenceProperty(MapReduceJob, collection_name="params")
    param = db.ReferenceProperty(MapperParam, collection_name="mapped_params")
        
    
## Proto Inserts
class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=AnalyzerEngine,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=False,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique name of analyzer engine.',keyid_use=None,keyparent_use=None))

        self.models.append(self.P(_class=AnalyzerTemplate,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))

        self.models.append(self.P(_class=MapReduceJob,
                                    direct_parent=db.Key.from_path('P','DataJob'),ancestry_path=['DataJob'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=MapReduceJobParam,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Name for param.',keyid_use=None,keyparent_use='Job that owns param and value.'))
        
        return self.models

    def base(self):
        
        self.models.append(AnalyzerEngine(key_name='object',
                            description='Extracts and creates entities from submitted data.',
                            handler_path='ProvidenceClarity.api.analyzer.object'))
                            
        self.models.append(AnalyzerEngine(key_name='relation',
                            description='Extracts and creates relationships between submitted entities.',
                            handler_path='ProvidenceClarity.api.analyzer.relation'))
                            
        self.models.append(AnalyzerEngine(key_name='stat',
                            description='Generates graph segments and relates entities beyond layer 2 relationships.',
                            handler_path='ProvidenceClarity.api.analyzer.stat'))
        

        return self.models


    def clean(self):
        
        self.models.append(self.P.get_by_key_name('AnalyzerEngine'))
        self.models.append(self.P.get_by_key_name('AnalyzerTemplate'))
        self.models.append(self.P.get_by_key_name('MapReduceJob'))
        self.models.append(self.P.get_by_key_name('MapReduceJobParam'))
        
        return self.models