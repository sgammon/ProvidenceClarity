from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.util import CreatedModifiedMixin


class ServiceAdapter(Model, CreatedModifiedMixin):
    
    """ Describes a service adapter in the services/ directory. Interfaces P/C with an external service or data source. """
    
    name = db.StringProperty()
    description = db.TextProperty()
    homepage = db.LinkProperty()
    docs = db.LinkProperty()
    

class ServiceRequest(Model, CreatedModifiedMixin):
    
    """ Represents a unique request issued to a ServiceAdapter. """
    
    adapter = db.ReferenceProperty(ServiceAdapter, collection_name="requests")
    result = db.StringProperty(choices=['success','failure'])
    request = db.TextProperty()
    response = db.TextProperty()
    
    
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=ServiceAdapter,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=False,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique service name.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=ServiceRequest,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,uses_keyname=False,uses_parent=True,uses_id=True,
                                   created_modified=True,keyname_use=None,keyid_use='Unique number for request.',keyparent_use='Service adapter request was issued to.'))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('ServiceAdapter'))
        self.models.append(self.P.get_by_key_name('ServiceRequest'))
        
        return self.models