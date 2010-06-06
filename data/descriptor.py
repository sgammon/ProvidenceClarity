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
    pass
    
class CachingDescriptor(D):
    """ Describes status and configuration of caching for a model or kind. """
    pass
    
class StatDescriptor(D):
    """ Describes status and configuration of statistics generation for a model or kind. """
    pass
    
class RevisionDescriptor(D):
    """ Describes revision history and increments revision count. """
    pass
    
class SourceDescriptor(D):
    """ Describes a source for this data point. """
    pass
    
class StorageRefDescriptor(D):
    """ Describes this data point as it exists in another storage system. """
    pass