from google.appengine.ext import db
from google.appengine.api import datastore

from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.api.data.proto import ProtoModel
from ProvidenceClarity.data.core.expando import Expando
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util
from ProvidenceClarity.data.util import CreatedModifiedMixin

from ProvidenceClarity.decorators.data import QueuedTransaction

class E(PolyModel, ProtoModel, CreatedModifiedMixin):
    
    """ A basic unit of real system data. """
    
    _E_ALWAYS_INDEXED = ['primary_display_text','keywords']
    _E_INDEXED = []
    
    ## Display text fields
    primary_display_text = db.StringProperty(indexed=True,verbose_name='Primary Text')
    keywords = util.NormalizedStringListProperty(indexed=True,verbose_name='Keywords')
    
    ## Internal Pointers
    _natural_kind_e = None
    _natural_kind_p = False
    
    ## Caching
    natural_kind = util.CachedProtobuf()
    descriptors = util.CachedProtobufList()
    
    
    def _entityIndexedProperties(self):
        return list(self._E_INDEXED+self._E_ALWAYS_INDEXED)
    
    def has_natural_kind(self):
        
        if self._natural_kind_p == False:
            return None
            
        else:
            if isinstance(self._natural_kind_e, db.Model):
                return self._natural_kind_e
            else:
                self._natural_kind_e = None
                self._natural_kind_p = False
                return None
        
    @QueuedTransaction('entityCreate')
    def put(self, **kwargs):
        return False
        
    @QueuedTransaction('entityDelete')
    def delete(self, **kwargs):
        return False
    

class NE(Expando):

    """ A reduced-down expando meant for temporary storage as a CachedProtobuf. """
    
    data_class_path = db.StringProperty(name='_data_class_path',indexed=True)


## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):

        self.models.append(self.P(_class=E,name=['Entity'],
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('E'))
        
        return self.models