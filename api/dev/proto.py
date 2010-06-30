from . import Dev
from data.proto import P

class ProtoBase(Dev):
    
    def insert():
        
        models = []

        models.append(P(key_name='P',name=['Prototype'],description='Describes a data kind\'s schema, including properties, property types, and details about whether it is abstract or derived.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=False,uses_keyname=True,uses_parent=True,uses_id=False,
                        created_modified=True,keyname_use='System data kind name.',keyid_use=None,keyparent_use=None
                        fields=['name','description','parent','abstract','derived','is_data','fields','field_types'],
                        field_types=['str_list','text','self_ref','bool','bool','bool','str_list','str_list']))
                    
        models.append(P(key_name='E',name=['Entity'],description='A basic, abstract unit of system data. Everything that can be represented by a single record inherits from Entity.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=True,created_modified=True,
                        keyname_use='_VARIABLE_',keyparent_use='_VARIABLE_',ancestry_path=[],keyid_use='_VARIABLE_',
                        fields=['primary_display_text','display_text','modified','created'],
                        field_types=['str','str_list','created','modified']))
                    
        models.append(P(key_name='R',name=['Relation'],description='Represents a relation between two Entity records. Relation kind represents the type of relationship, while individual records store details of the connection.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                        keyname_use='Variable, depending on child protos.',keyparent_use='Used for direction connections (parent is source).',
                        fields=['entities','origin','end'],
                        field_types=['e_ref_list','e_ref','e_ref']))
                    
        models.append(P(key_name='D',name=['Descriptor'],description='A small unit of data that can be attached to other data points. Can be extended and created on the fly.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                        keyname_use='Name of descriptor.',keyparent_use='Data point descriptor is attached to.',
                        fields=['parent_key'],
                        field_types=['str']))
                    
        models.append(P(key_name='I',name=['Index'],description='A normalized, high-level index that can be extended and created/generated on the fly.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,created_modified=True,
                        keyname_use='Variable, depending on child protos.',keyparent_use='Proto this indexes, if applicable.',
                        fields=['name','description'],
                        field_types=['str','text']))
                    
        models.append(P(key_name='C',name=['Cache'],description='Model structure for temporarily storing hard-to-retrieve or hard-to-generate data for easy access.',
                        direct_parent=None,ancestry_path=[],abstract=True,derived=False,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=True,created_modified=True,
                        keyname_use='Variable, depending on child protos.',keyparent_use='Proto or data point to be cached.',keyid_use='Variable, depending on child protos.',
                        fields=['expiration_enabled','expiration_datetime','modified','created'],
                        field_types=['bool','datetime','modified','created']))
    
        return models
        
    def clean():
        
        models = []
        
        models.append(P.get_by_key_name('P'))
        models.append(P.get_by_key_name('E'))
        models.append(P.get_by_key_name('R'))
        models.append(P.get_by_key_name('D'))
        models.append(P.get_by_key_name('I'))
        models.append(P.get_by_key_name('C'))
        
        return models                                        