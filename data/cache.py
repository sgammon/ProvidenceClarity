from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.util import CreatedModifiedMixin

class C(PolyModel, CreatedModifiedMixin):

    ## Expiration items
    expiration_enabled = db.BooleanProperty(required=True,default=True,verbose_name="Auto-Expiration?")
    expiration_datetime = db.DateTimeProperty(required=False,verbose_name="Expiration Date/Time")
    
class NC(Model, CreatedModifiedMixin):
    pass