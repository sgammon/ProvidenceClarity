from google.appengine.ext import db
from ProvidenceClarity.data.entity import E
#from ProvidenceClarity.data.relationship import R
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util

## +=+=+ Master class - retrieves referenced PC data object only on get instead of fetch.
class PCRef(db.ReferenceProperty):
    pass

## +=+=+ Entity reference (E)
class ERef(PCRef):

    def __init__(self, **kwds):
        super(ERef, self).__init__(E, **kwds)
        
class ERefList(util.ListProperty):

    def __init__(self, **kwds):
        super(ERefList, self).__init__(db.Key, **kwds)
    
## +=+=+ Connection reference (C)
#class RRef(PCRef):
#
#    def __init__(self, **kwds):
#        super(RRef, self).__init__(R, **kwds)
#        
#class RRefList(util.ListProperty):
#
#    def __init__(self, **kwds):
#        super(RRefList, self).__init__(db.Key, **kwds)