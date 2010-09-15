from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.core.polymodel import PolyModel
from ProvidenceClarity.data.core.properties import util, reference
from ProvidenceClarity.data.descriptor import DescriptorModel ## @TODO: move this to descriptor api under data
from ProvidenceClarity.api.data.proto import ProtoModel

class R(PolyModel, ProtoModel, DescriptorModel):
    
    """ Describes a relationship between two entities. """
    
    ## Relationship items
    entities = reference.ERefList(verbose_name="Entity Path")
    origin = reference.ERef(verbose_name="Origin",collection_name="r_origin")
    end = reference.ERef(verbose_name="End",collection_name="r_end")
    

## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=R,name=['Relation'],description='Describes a relationship between two entities.',
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models


    def clean(self):
        
        self.models.append(self.P.get_by_key_name('R'))
        
        return self.models