from google.appengine.ext import db
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.properties.util import NormalizedStringListProperty

### proto caching
proto_list = {}

### types list
types_list = ['str','text','bool','int','key','float','str_list','int_list','float_list','key_list','ref','self_ref','e_ref','e_ref_list','r_ref','r_ref_list','created','modified','date','time','datetime']

##### ### Master Proto Classes ### #####

class P(Model, CreatedModifiedMixin):
    """ Prototype for a system data point, which includes E (entities), C (connections), I (indexes), C (caches), and D (descriptors). """

    ## Naming details (key_name is always official kind name)
    name = db.StringListProperty(required=True,indexed=True,verbose_name="Name")
    description = db.TextProperty(required=False,indexed=False,verbose_name="Description")

    ## Ancestor path
    direct_parent = db.SelfReferenceProperty(required=True,default=None,indexed=True,collection_name="children",verbose_name="Direct Parent")
    ancestry_path = db.ListProperty(basestring,required=True,default=None,indexed=True,verbose_name="Ancestry Path")
    abstract = db.BooleanProperty(required=True,default=False,indexed=False,verbose_name="Abstract?")
    
    ## Data Ancestry/Usage Properties
    derived = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Derived?")
    is_data = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Is data?")
    poly_model = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Is poly?")
    uses_keyname = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses key name?")
    uses_parent = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses parent?")
    uses_id = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Uses key id?")
    created_modified = db.BooleanProperty(required=True,default=False,indexed=True,verbose_name="Created/modified?")

    ## Special Properties
    keyname_use = db.StringProperty(required=False,default=None,indexed=False,verbose_name="Key Name Usage")
    keyid_use = db.StringProperty(required=False,default=None,indexed=False,verbose_name="Key ID Usage")
    keyparent_use = db.StringProperty(required=False,default=None,indexed=False,verbose_name="Key Parent Usage")

    ## List of fields and field types
    fields = NormalizedStringListProperty(required=True,indexed=True,verbose_name="Proto Fields")
    field_types = NormalizedStringListProperty(required=True,choices=types_list,indexed=False,verbose_name="Field Types")
    
    
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
        if (len(proto.fields) > 0) AND (len(proto.field_types) > 0):
            dat = {}
            for item in range(0,len(proto.fields)-1):
                dat[proto.fields[item]] = proto.field_types[item]
            return dat
        return None