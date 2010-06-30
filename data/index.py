from google.appengine.ext import db
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel

class I(PolyModel):

    ## index naming, etc
    name = db.StringProperty(required=True,indexed=True)
    description = db.TextProperty(required=True,indexed=False)
    normalized = db.BooleanProperty(default=True,indexed=True)
    
class NI(Model):
    pass