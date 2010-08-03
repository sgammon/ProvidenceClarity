from google.appengine.ext import db
from ProvidenceClarity.api.data import DataManager
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.properties.util import NormalizedStringListProperty

### proto caching
proto_list = {}

##### ### Master Proto Classes ### #####

class P(Model, CreatedModifiedMixin):
    
    """ Prototype for a system data point, which includes E (entities), C (connections), I (indexes), C (caches), D (descriptors), and all child protos. """

    ## Unstored Properties
    _class = None

    ## Naming details (key_name is always official kind name)
    name = db.StringListProperty(required=True,indexed=True,verbose_name="Name")
    description = db.TextProperty(required=False,indexed=False,verbose_name="Description")

    ## Ancestor path
    direct_parent = db.SelfReferenceProperty(required=False,default=None,indexed=True,collection_name="children",verbose_name="Direct Parent")
    ancestry_path = db.ListProperty(basestring,required=True,default=None,indexed=True,verbose_name="Ancestry Path")
    abstract = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Abstract?")
    
    ## Package details
    package = db.ListProperty(basestring,required=True,default=None,indexed=True,verbose_name="Parent Package")
    package_path = db.StringProperty(required=False,default='',indexed=False,verbose_name="Package Path")
    
    ## Data Ancestry/Usage Properties
    derived = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Derived?")
    is_data = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Is data?")
    poly_model = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Is poly?")
    expando = db.BooleanProperty(required=False,default=False,indexed=True,verbose_name="Is expando?")
    uses_keyname = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses key name?")
    uses_parent = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses parent?")
    uses_id = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses key id?")
    created_modified = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Created/modified?")

    ## Special Properties
    keyname_use = db.StringProperty(required=False,default="",indexed=False,verbose_name="Key Name Usage")
    keyid_use = db.StringProperty(required=False,default="",indexed=False,verbose_name="Key ID Usage")
    keyparent_use = db.StringProperty(required=False,default="",indexed=False,verbose_name="Key Parent Usage")

    ## List of fields and field types
    field_list = NormalizedStringListProperty(required=True,indexed=False,verbose_name="Proto Fields")
    field_types = NormalizedStringListProperty(required=True,indexed=False,verbose_name="Field Types")
    
    def __init__(self, *args, **kwargs):
        
        ## If class is given, automatically set description, name, and key_name
        if '_class' in kwargs:
            self._class = kwargs['_class']
            kwargs['key_name'] = self._class.__name__

            kwargs['package'] = self._class.__module__.split('.')

            kwargs['package_path'] = self._class.__module__
            kwargs['description'] = str(self._class.__doc__).strip()
            
            if 'name' in kwargs and isinstance(kwargs['name'], list):
                kwargs['name'].append(self._class.__name__)
                
            else:
                kwargs['name'] = [self._class.__name__]
            
        super(P, self).__init__(*args, **kwargs)
    
    
class ProtoModel:
    """ Provides methods and properties for models that are proto-enabled. """

    # grabbed protomodel
    __proto = None

    @classmethod
    def getProto(cls):
        global proto_list
        
        # check class first
        if cls.__proto is not None:
            return cls.__proto
        
        # check cache first
        if cls.__name__ in proto_list:
            cls.__proto = proto_list[cls.__name__]
            return proto_list[cls.__name__]
        else:
            proto_list[cls.__name__] = P.get_by_key_name(cls.__name__)
            cls.__proto = proto_list[cls.__name__]

        return cls.__proto
        
    @classmethod
    def getProtoFields(cls):
        proto = cls.getProto()
        if (len(proto.fields) > 0) and (len(proto.field_types) > 0):
            dat = {}
            for item in range(0,len(proto.fields)-1):
                dat[proto.fields[item]] = proto.field_types[item]
            return dat
        return None
        
        
## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=P,name=['Proto'],
                                    direct_parent=None,ancestry_path=[],abstract=False,derived=False,is_data=False,poly_model=True,uses_keyname=False,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use=None,keyid_use=None,keyparent_use=None))
        
        return self.models
    

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('P'))
        
        return self.models