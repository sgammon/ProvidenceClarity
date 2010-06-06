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
    parent = db.SelfReferenceProperty(required=True,default=None,indexed=True,collection_name="children",verbose_name="Child Protos")
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
    keyname_use = db.StringProperty(required=False,indexed=False,verbose_name="Key Name Usage")
    keyid_use = db.StringProperty(required=False,indexed=False,verbose_name="Key ID Usage")
    keyparent_use = db.StringProperty(required=False,indexed=False,verbose_name="Key Parent Usage")

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
        
##### ###   Built-In Protos (for dev or first data)   ### #####

def devAddProtos():
    
    models = []

    models.append(P(key_name='P',name=['Prototype'],description='Describes a data kind\'s schema, including properties, property types, and details about whether it is abstract or derived.',
                    abstract=True,derived=False,is_data=False,poly_model=False,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                    keyname_use='System data kind name.',keyparent_use='',
                    fields=['name','description','parent','abstract','derived','is_data','fields','field_types'],
                    field_types=['str_list','text','self_ref','bool','bool','bool','str_list','str_list']))
                    
    models.append(P(key_name='E',name=['Entity'],description='A basic, abstract unit of system data. Everything that can be represented by a single record inherits from Entity.',
                    abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=True,created_modified=True,
                    keyname_use='Variable, depending on child protos.',keyparent_use='',keyid_use='',                    
                    fields=['primary_display_text','display_text','modified','created'],
                    field_types=['str','str_list','created','modified']))
                    
    models.append(P(key_name='R',name=['Relation'],description='Represents a relation between two Entity records. Relation kind represents the type of relationship, while individual records store details of the connection.',
                    abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                    keyname_use='Variable, depending on child protos.',keyparent_use='Used for direction connections (parent is source).',
                    fields=['entities','origin','end'],
                    field_types=['e_ref_list','e_ref','e_ref']))
                    
    models.append(P(key_name='D',name=['Descriptor'],description='A small unit of data that can be attached to other data points. Can be extended and created on the fly.',
                    abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                    keyname_use='Name of descriptor.',keyparent_use='Data point descriptor is attached to.',
                    fields=['parent_key'],
                    field_types=['str']))
                    
    models.append(P(key_name='I',name=['Index'],description='A normalized, high-level index that can be extended and created/generated on the fly.',
                    abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                    keyname_use='Variable, depending on child protos.',keyparent_use='Proto this indexes, if applicable.',
                    fields=['name','description'],
                    field_types=['str','text']))
                    
    models.append(P(key_name='C',name=['Cache'],description='Model structure for storing hard-to-retrieve or hard-to-generate data for easy access.',
                    abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=True,created_modified=True,
                    keyname_use='Variable, depending on child protos.',keyparent_use='Proto or data point to be cached.',keyid_use='Variable, depending on child protos.',
                    fields=['expiration_enabled','expiration_datetime','modified','created'],
                    field_types=['bool','datetime','modified','created']))
    
    