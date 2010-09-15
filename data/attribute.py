from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.api.data.proto import ProtoModel
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.polymodel import PolyModel


class A(PolyModel, ProtoModel, CreatedModifiedMixin):
    
    """ Describes a generic attribute that can be applied to another data point. """
    
    name = db.StringProperty(indexed=True)

    
## Proto Inserts
class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(name=['A','Attribute'],_class=A,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('A'))
        
        return self.models