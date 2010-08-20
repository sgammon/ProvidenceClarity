__all__ = ['cacher','indexer','proto']

import logging
from google.appengine.ext import db, blobstore
from ProvidenceClarity.main import PCController
from ProvidenceClarity.api.data import exceptions
from ProvidenceClarity.api.util import import_helper
from ProvidenceClarity.data.core.natural import NaturalKind

from ProvidenceClarity.data.core.properties.polymodel import _ClassKeyProperty, _ModelPathProperty

## Property class mappings
class_map = {

    # default google-provided properties
    db.StringProperty.__name__:'string',
    db.ByteStringProperty.__name__:'bytestring',
    db.BooleanProperty.__name__:'bool',
    db.IntegerProperty.__name__:'int',
    db.FloatProperty.__name__:'float',
    db.DateTimeProperty.__name__:'datetime',
    db.DateProperty.__name__:'date',
    db.TimeProperty.__name__:'time',
    db.ListProperty.__name__:'list',
    db.StringListProperty.__name__:'str_list',
    db.ReferenceProperty.__name__:'ref',
    db.SelfReferenceProperty.__name__:'self_ref',
    blobstore.BlobReferenceProperty.__name__:'blob_ref',
    db.UserProperty.__name__:'user',
    db.BlobProperty.__name__:'blob',
    db.TextProperty.__name__:'text',
    db.CategoryProperty.__name__:'category',
    db.LinkProperty.__name__:'link',
    db.EmailProperty.__name__:'email',
    db.GeoPtProperty.__name__:'geo_pt',
    db.IMProperty.__name__:'im',
    db.PhoneNumberProperty.__name__:'phone',
    db.PostalAddressProperty.__name__:'postal_addr',
    db.RatingProperty.__name__:'rating',

}

OTHER_TYPE_FLAG = '_other_'
            
# Abstract class for data-handling API modules
class DataController(PCController):

    @classmethod
    def import_model(cls, classpath):

        logging.info('===== Import Model Request =====')

        if isinstance(classpath, list):
            logging.info('Classpath is list: '+'.'.join(classpath[0:-1])+' with endpoint '+classpath[-1])
            imported_class = import_helper('.'.join(classpath[0:-1]),classpath[-1])
        
        elif isinstance(classpath, (str, unicode)):
            logging.info('Classpath is string: '+classpath)
            imported_class = import_helper(classpath)
            
        else:
            logging.critical('Classpath is neither list nor str but actually '+str(type(classpath))+'.')
            return False
        
        return imported_class
        
        
    @classmethod
    def generateNaturalKind(cls, entity, softfail=False, **kwargs):
        
        from ProvidenceClarity.data.entity import E
        
        ## only accepts polymodel instances
        if hasattr(entity, '_PC_MODEL_BRANCH'):
            if getattr(entity, '_PC_MODEL_BRANCH') == '_POLY_':
                if entity.class_key()[-1] == 'E':
                    if softfail is True:
                        return (entity, None)
                    else:
                        raise exceptions.InvalidPolyInput('Cannot convert root E to a natural kind.') ## @TODO: String localization
                else:
                    pass
            else:
                if softfail is True:
                    return (entity, None)
                else:
                    raise exceptions.InvalidPolyInput('Invalid PC model branch.')
        
        k = entity.key()
        
        if isinstance(k.id_or_name(), str): ## if it has a keyname, namespace and honor it
            _e_key = db.Key.from_path('E', entity._getNamespacedKeyName(k.name()))
            _n_key = db.Key.from_path(entity.class_key()[-1], k.name())
        else:
            start, end = db.allocate_ids(db.Key.from_path('E',1), 1)
            _e_key = db.Key.from_path('E',start)
            
            start, end = db.allocate_ids(db.Key.from_path(entity.class_key()[-1], 1), 1)
            _n_key = db.Key.from_path(entity.class_key()[-1], start, parent=_e_key)
                
        if 'key_name' in kwargs:
            del kwargs['key_name']
                
        n_prop = {}
        e_prop = entity.properties()
        for item in e_prop:

            if e_prop[item].__class__ in [_ClassKeyProperty, _ModelPathProperty]:
                pass ## ignore classkey and modelpath properties

            elif e_prop[item].__class__ == db.ReferenceProperty:
                e_prop[item] = db.ReferenceProperty(collection_name=item+'_n')
            
            else:
                n_prop[item] = e_prop[item]

        ## create and instantiate model class
        ClassObj = type(entity.class_key()[-1], (NaturalKind,), n_prop)

        natural_kind_record = ClassObj(key=_n_key, **kwargs)
        t_entity = E(key=_e_key) ## create trimmed entity
        
        for prop in n_prop:
            setattr(natural_kind_record, prop, getattr(entity, prop))

            if prop in entity._entityIndexedProperties():
               setattr(t_entity, prop, getattr(entity, prop)) ## move indexed properties over to new Entity
        
        return t_entity, natural_kind_record


# Utility class for proto and dev structure
class DataManager(object):
    
    models = []
    P = None
    
    def __init__(self):
        from ProvidenceClarity.data.proto import P
        self.P = P
    
    def do_test(self):
        logging.info('MANAGER: TEST COMPLETE!')
    
    ## passed down to child classes
    def insert(self):
        pass
    
    ## passed down to child classes
    def clean(self):
        pass
        
    def sanitize(self, data):
        
        """ Clears empty models from a list. """
        
        if isinstance(data, list):
            
            index = data[:]
            
            for model in index:
                if model is None:
                    data.remove(model)
                    
            return data
        
        else:
            return False ## graceful fail
                
        
    def do_insert(self):
        
        self.models = []
        self.models = self.insert()

        if isinstance(self.models, list):
            
            for model in self.models:
                
                if hasattr(model, '_class') and model._class is not None:
                
                    properties = model._class.properties()
                
                    property_names = []
                    property_types = []
                
                    for prop in properties:
                    
                        ## Skip anything that begins with an underscore
                        if prop[0] == '_':
                            continue
                    
                        ## Append to the names list
                        property_names.append(prop)
                    
                        ## If it's in the classmap
                        if properties[prop].__class__.__name__ in class_map:
                            property_types.append(class_map[properties[prop].__class__.__name__])
                        
                        ## If it's a custom property with the storage name attached...
                        elif hasattr(properties[prop], '_storage_type_name'):
                            property_types.append(getattr(properties[prop], '_storage_type_name'))
                    
                        ## Default to OTHER_TYPE_FLAG
                        else:
                            property_types.append(OTHER_TYPE_FLAG)
                        
                    model.field_list = property_names
                    model.field_types = property_types
            
            try:
                res = db.put(self.sanitize(self.models))
                
            except:
                return False
                
            return (True,res)
                
            
    def do_clean(self):

        self.models = []
        self.models = self.clean()
        
        
        if isinstance(self.models, list):
            
            try:
                res = db.delete(self.sanitize(self.models))
            
            except:
                return False
                
            return (True,res)
            
    def do_base(self):
        
        self.models = []
        
        if hasattr(self, 'base'):
            self.models = self.base()
            if isinstance(self.models, list):
            
                return db.put(self.models)          
        else:
            pass
    