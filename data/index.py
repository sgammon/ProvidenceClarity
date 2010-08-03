from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel

class I(PolyModel):

    """ Describes a dynamic system index. """

    ## index naming, etc
    name = db.StringProperty(required=True,indexed=True)
    description = db.TextProperty(required=True,indexed=False)
    normalized = db.BooleanProperty(default=True,indexed=True)
    
class NI(Model):
    
    """ Describes a normalized index that transcends different index types. """
    
    pass
    
    
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
    
        self.models.append(self.P(_class=I,name=['Index'],
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=NI,name=['NormalizedIndex'],
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('I'))
        self.models.append(self.P.get_by_key_name('NI'))
        
        return self.models    