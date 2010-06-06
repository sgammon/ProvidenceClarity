from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util, reference
from ProvidenceClarity.data.proto import ProtoModel

class R(PolyModel, ProtoModel):
    
    ## Relationship items
    entities = reference.EReferenceList(verbose_name="Entity Path")
    origin = reference.EReference(verbose_name="Origin")
    end = reference.EReference(verbose_name="End")