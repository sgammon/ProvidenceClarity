from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.util import CreatedModifiedMixin
    

class ServiceAdapter(Model, CreatedModifiedMixin):
    
    """ Describes a service adapter in the services/ directory. Interfaces P/C with an external service or data source. """
    
    name = db.StringProperty()
    description = db.TextProperty()
    homepage = db.LinkProperty()
    docs = db.LinkProperty()
    adapter_handler = db.StringProperty()
    requires_auth = db.BooleanProperty()


class AuthKey(PolyModel, CreatedModifiedMixin):
    
    """ Describes an abstract key used to connect to an external service. """
    
    service = db.ReferenceProperty(ServiceAdapter, collection_name='auth_keys')
    global_use_limit = db.IntegerProperty(default=0)
    daily_use_limit = db.IntegerProperty(default=0)
    name = db.StringProperty()
    value = db.TextProperty()
    expires = db.BooleanProperty()
    expiration = db.DateTimeProperty()
    

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
                                   
        self.models.append(self.P(_class=AuthKey,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=ServiceRequest,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,uses_keyname=False,uses_parent=True,uses_id=True,
                                   created_modified=True,keyname_use=None,keyid_use='Unique number for request.',keyparent_use='Service adapter request was issued to.'))
        
        return self.models
        
        
    def base(self):
        
        self.models.append(ServiceAdapter(key_name='freebase',name='Freebase',description='Open schema-powered datastore used in PC for disambiguation and for general information on inputted entities.',homepage=db.Link('http://www.freebase.com/'),docs=db.Link('http://wiki.freebase.com/wiki/Main_Page')))
        self.models.append(ServiceAdapter(key_name='googlenews',name='Google News',description='News aggregation service used in PC for finding articles related to entities.',homepage=db.Link('http://news.google.com'),docs=db.Link('http://code.google.com/apis/ajaxsearch/')))
        self.models.append(ServiceAdapter(key_name='opencalais',name='OpenCalais',description='Semantic analysis service provided by Reuters and used in PC for pulling entities out of unstructured information.',homepage=db.Link('http://http://www.opencalais.com/'),docs=db.Link('http://www.opencalais.com/documentation/opencalais-documentation')))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('ServiceAdapter'))
        self.models.append(self.P.get_by_key_name('AuthKey'))
        self.models.append(self.P.get_by_key_name('ServiceRequest'))
        
        return self.models