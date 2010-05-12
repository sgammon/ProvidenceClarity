try: import pc_config except ImportError: pass
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util

class E(PolyModel):
    
    ## Constants available for override
    INDEX_DISPLAY_TEXT = True
    OTHER_INDEX_FIELDS = []
    SPECIAL_FIELDS = {'title':None,'summary':None,'published':None,
                      'author':None,'link':None,'source':None,'digested':None}    

    ## Display text fields
    primary_display_text = db.StringProperty(indexed=True,verbose_name='Primary Text')
    display_text = util.NormalizedStingListProperty(indexed=True,verbose_name='Display Text')
    
    ## Index fields
    last_indexed = util.DateTimeProperty(default=None,verbose_name='Display Text')
    marked_for_index = db.BooleanProperty(default=pc_config.get('index_on_put','data',False),verbose_name='Mark for Indexing')
    
    ## Audit trail fields
    modified = util.DateTimeProperty(auto_now=True,verbose_name='Modified')
    created = util.DateTimeProperty(auto_now_add=True,verbose_name='Created')