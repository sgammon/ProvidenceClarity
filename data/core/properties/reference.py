from google.appengine.ext import db
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util

## +=+=+ Master class - retrieves referenced PC data object only on get instead of fetch.
class PCRef(db.ReferenceProperty):
    pass

class PCReverseRef(db.ReverseReferenceProperty):
    pass

## +=+=+ Entity reference (E)
class ERef(PCReferenceProperty):
    pass
    
class ReverseERef(PCReverseReferenceProperty):
    pass
    
class ERefList(util.ListProperty):
    pass
    
## +=+=+ Connection reference (C)
class RRef(PCReferenceProperty):
    pass
    
class ReverseRRef(PCReverseReferenceProperty):
    pass
    
class RRefList(util.ListProperty):
    pass