from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util, reference
from ProvidenceClarity.data.proto import ProtoModel
from ProvidenceClarity.data.descriptor import DescriptorModel
from ProvidenceClarity.data.util import CreatedModifiedMixin

class R(PolyModel, ProtoModel, DescriptorModel, CreatedModifiedMixin):
    
    ## Relationship items
    entities = reference.EReferenceList(verbose_name="Entity Path")
    origin = reference.EReference(verbose_name="Origin")
    end = reference.EReference(verbose_name="End")