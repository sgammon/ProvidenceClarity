from ProvidenceClarity.data.core.proto import ProtoModel
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util
from ProvidenceClarity.data.util import CreatedModifiedMixin

class E(PolyModel, ProtoModel, CreatedModifiedMixin):
    
    ## Constants available for override
    INDEX_DISPLAY_TEXT = True
    OTHER_INDEX_FIELDS = []
    SPECIAL_FIELDS = {'title':None,'summary':None,'published':None,
                      'author':None,'link':None,'source':None,'consumed_date':None}    

    ## Display text fields
    primary_display_text = db.StringProperty(indexed=True,verbose_name='Primary Text')
    display_text = util.NormalizedStingListProperty(indexed=True,verbose_name='Display Text')
    
    ## Index fields
    last_indexed = util.DateTimeProperty(default=None,verbose_name='Display Text')
    marked_for_index = db.BooleanProperty(default=pc_config.get('index_on_put','data',False),verbose_name='Mark for Indexing')
    
    def graph():
        pass
        
    def connections():
        pass
        
    def descriptors():
        pass
        
    def index():
        pass