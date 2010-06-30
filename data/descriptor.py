from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.proto import ProtoModel
from ProvidneceClarity.data.util import CreatedModifiedMixin

##### ### Master Descriptor Classes ### #####

class D(PolyModel, ProtoModel, CreatedModifiedMixin):

    ALLOW_MULTI = True # allow multi descriptors per data point
    ALLOW_OVERRIDE = True # allow override on specific data points over kind descriptors
    
    ## parent attachment
    parent_key = db.StringProperty(required=True,indexed=True,verbose_name="Parent Key")

class DescriptorModel:
    """ Provides methods and properties for models that are descriptor-enabled. """    
    pass

##### ###   Built-In Descriptors   ### #####

class IndexingDescriptor(D):
    """ Describes status and configuration of indexing for a model or kind. """
    last_indexed = util.DateTimeProperty(default=None,verbose_name='Display Text')
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