from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.expando import Expando
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.util import CreatedModifiedMixin


class C(PolyModel, CreatedModifiedMixin):
    
    """ Basic caching model. """

    ## Expiration items
    expiration_enabled = db.BooleanProperty(required=True,default=True,verbose_name="Auto-Expiration?")
    default_expiration = db.IntegerProperty(required=True,default=86400,verbose_name="Default Expiration")

    
class NC(Model, CreatedModifiedMixin):
    
    """ A normalized cache that transcends properties of all proto-type caches. """    
    pass
    

class CachedItem(db.Expando):
    
    """ An item in a cache. """
    
    cache = db.ReferenceProperty(C, collection_name="items")


class NormalizedObject(Expando):
    
    """ An object not meant to be stored, but compressed to a Protobuf. A midway model used in between encoding and decoding. """
    
    data_class_path = db.StringProperty(name='_data_class_path')
    
    def put(self):
        raise NotImplementedError('NormalizedObject is meant for entity storage and is not allowed to be stored.')
    

## Proto Inserts
class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=C,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=NormalizedObject,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=True,
                                   created_modified=False,keyname_use='Adopts key name of encoded object.',keyid_use='Adopts ID of encoded object.',keyparent_use='Adopts parent of encoded object.'))
        
        self.models.append(self.P(_class=CachedItem,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=True,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Key of the cached item.',keyid_use=None,keyparent_use='Parent cache record.'))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('C'))
        self.models.append(self.P.get_by_key_name('NC'))
        self.models.append(self.P.get_by_key_name('CachedItem'))
        
        return self.models