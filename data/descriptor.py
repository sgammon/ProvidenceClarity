from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.proto import ProtoModel

##### ### Master Descriptor Classes ### #####

class D(PolyModel, ProtoModel):

    """ A descriptor that can be attached to another data record. """

    ALLOW_MULTI = True # allow multi descriptors per data point
    ALLOW_OVERRIDE = True # allow override on specific data points over kind descriptors
    
    ## parent attachment
    record_parent = db.StringProperty(required=True,indexed=True,verbose_name="Parent Key")

class DescriptorModel:
    """ Provides methods and properties for models that are descriptor-enabled. """    
    pass

##### ###   Built-In Descriptors   ### #####

class IndexingDescriptor(D):
    """ Describes status and configuration of indexing for a model or kind. """
    last_indexed = db.DateTimeProperty(default=None,verbose_name='Last Indexed')
    marked_for_index = db.BooleanProperty(verbose_name='Mark for Indexing')
    
class CachingDescriptor(D):
    """ Describes status and configuration of caching for a model or kind. """
    do_cache = db.BooleanProperty(default=True,verbose_name="Enable Cache")
    
class StatDescriptor(D):
    """ Describes status and configuration of statistics generation for a model or kind. """
    node_value = db.FloatProperty(default=1.0)
    node_multiplier = db.FloatProperty(default=1.0)
    
class RevisionDescriptor(D):
    """ Describes revision history and increments revision count. """
    pass
    
class SourceDescriptor(D):
    """ Describes a source for this data point. """
    pass
    
class StorageRefDescriptor(D):
    """ Describes this data point as it exists in another storage system. """
    pass
    
class ExtSchemaDescriptor(D):
    """ Links a record to an external schema. """
    pass
    
    
class CachedDescriptor(D):
    """ Indicates whether a record has cached items. """
    
    cache_key = db.StringProperty()
    cache_reference = db.ReferenceProperty()
    
    
class FreebaseSchema(ExtSchemaDescriptor):
    """ Links a record to a Freebase type. """
    
    schema_set = db.ListProperty(basestring)
    schema_path = db.StringProperty()
    
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):

        self.models.append(self.P(_class=D,name=['Descriptor'],
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=IndexingDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=CachingDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=StatDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=RevisionDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=SourceDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=StorageRefDescriptor,
                                    direct_parent=db.Key.from_path('Proto','D'),ancestry_path=['D'],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('D'))
        self.models.append(self.P.get_by_key_name('IndexingDescriptor'))
        self.models.append(self.P.get_by_key_name('CachingDescriptor'))
        self.models.append(self.P.get_by_key_name('StatDescriptor'))
        self.models.append(self.P.get_by_key_name('RevisionDescriptor'))
        self.models.append(self.P.get_by_key_name('SourceDescriptor'))
        self.models.append(self.P.get_by_key_name('StorageRefDescriptor'))
        
        return self.models