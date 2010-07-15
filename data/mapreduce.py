from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.model import Model


class Mapper(Model, CreatedModifiedMixin):
    
    """ Describes a mapper defined in the mapreduce.yaml file. """
    
    name = db.StringProperty()
    input_reader = db.StringProperty(choices=['datastore','blobstore_line','blobstore_zip'])
    
class MapperParam(db.Expando):
    
    """ Describes a parameter for a mapper defined in the mapreduce.yaml file. """
    
    name = db.StringProperty()
    mapper = db.ReferenceProperty(Mapper, collection_name="params")
    

## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=Mapper,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique name for mapper.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=MapperParam,
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=False,expando=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Named parameter key.',keyid_use=None,keyparent_use='Namespacing for named parameter keys.'))
        
        return self.models


    def clean(self):
        
        self.models.append(P.get_by_key_name('Mapper'))
        self.models.append(P.get_by_key_name('MapperParam'))
        
        return self.models