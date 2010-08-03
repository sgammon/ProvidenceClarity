from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.proto import ProtoModel
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util
from ProvidenceClarity.data.util import CreatedModifiedMixin

class E(PolyModel, ProtoModel, CreatedModifiedMixin):
    
    """ A basic unit of real data. """
    
    ## Constants available for override
    INDEX_DISPLAY_TEXT = True
    OTHER_INDEX_FIELDS = []
    SPECIAL_FIELDS = {'title':None,'summary':None,'published':None,
                      'author':None,'link':None,'source':None,'consumed_date':None}

    ## Display text fields
    primary_display_text = db.StringProperty(indexed=True,verbose_name='Primary Text')
    display_text = util.NormalizedStringListProperty(indexed=True,verbose_name='Display Text')
    

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