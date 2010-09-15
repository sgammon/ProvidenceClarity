from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.expando import Expando


class SystemProperty(Expando, CreatedModifiedMixin):
    
    """ Describes a basic system property (similar to Microsoft Windows' registry). """
    
    name = db.StringProperty(indexed=True)
    module = db.StringListProperty(indexed=True)
    last_access = db.DateTimeProperty()

    
class TempSystemProperty(Expando, CreatedModifiedMixin):
    
    """ Describes a basic system property (similar to Microsoft Windows' registry) that deletes itself automatically. """
    
    max_lifetime = db.DateTimeProperty()
    expiration = db.DateTimeProperty()
    last_access = db.DateTimeProperty()
    
    
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=SystemProperty,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Named system property.',keyid_use=None,keyparent_use=None))
        
        self.models.append(self.P(_class=TempSystemProperty,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=True,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Named system property.',keyid_use=None,keyparent_use=None))
        
        return self.models
        
    
    def base(self):
        
        self.models.append(SystemProperty(key_name='proto_boot_done',name='proto_boot_done',module='api.data.proto.ProtoController'.split('.'),value=True))

        return self.models
        

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('SystemProperty'))
        self.models.append(self.P.get_by_key_name('TempSystemProperty'))
        
        return self.models