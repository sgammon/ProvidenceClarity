from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util, reference

class C(PolyModel):
    
    ## Connection items
    entities = reference.EReferenceList(verbose_name="Entity Path")
    origin = reference.EReference(verbose_name="Origin")
    end = reference.EReference(verbose_name="End")
    
    ## Summarized scoring
    score = db.FloatProperty(default=1.0,verbose_name="Summarized Score")
    multiplier = db.FloatProperty(default=0.1,verbose_name="Relationship Multiplier")
    
    ## Audit trail
    modified = util.DateTimeProperty(auto_now=True)
    created = util.DateTimeProeprty(auto_now_add=True)