from google.appengine.ext import db
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util

## +=+=+ Master class - retrieves referenced PC data object only on get instead of fetch.
class PCReferenceProperty(db.ReferenceProperty):
    pass

class PCReverseReferenceProperty(db.ReverseReferenceProperty):
    pass

## +=+=+ Entity reference (E)
class EReference(PCReferenceProperty):
    pass
    
class ReverseEReference(PCReverseReferenceProperty):
    pass
    
class EReferenceList(util.ListProperty):
    pass
    
## +=+=+ Connection reference (C)
class CReference(PCReferenceProperty):
    pass
    
class ReverseCReference(PCReverseReferenceProperty):
    pass
    
class CReferenceList(util.ListProperty):
    pass