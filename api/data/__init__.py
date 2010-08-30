__all__ = ['cacher','indexer','proto']

import logging, exceptions
from google.appengine.ext import db, blobstore
from google.appengine.api.labs import taskqueue
from ProvidenceClarity import PCController
from ProvidenceClarity.api.util import import_helper
from ProvidenceClarity.data.core import _PC_MODEL_BRANCH_POINTER, _PC_MODEL_BRANCH_POLY
from ProvidenceClarity.data.core.expando import Expando

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
    
    _subcontrollers = {'proto':['proto','ProtoController'],'tasks':['tasks','TaskController'],'transaction':['transaction','TransactionController']}
    
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
    def generateNaturalKind(cls, entity, softfail=False, nk_opts={}, **kwargs):
        
        if hasattr(entity, _PC_MODEL_BRANCH_POINTER):
            if getattr(entity, _PC_MODEL_BRANCH_POINTER) == _PC_MODEL_BRANCH_POLY:
                if hasattr(entity, 'class_key') and entity.class_key()[-1] == E.__name__:
                    if softfail is True:
                        return (entity, None)
                    else:
                        raise exceptions.InvalidPolyInput('Cannot convert root E to a natural kind.') ## @TODO: String Localization
                else:
                    if softfail is True:
                        return (entity, None)
                    else:
                        raise exceptions.InvalidPolyInput('Cannot convert entity with root other than __POLY__ to a natural kind.')
        try:
            ## Grab entity key name, if any
            if hasattr(entity, '_key_name'):
                pass #### LEFT OFF HERE!!!!! ###
                
        except:
            pass
        
    @classmethod
    def generateNaturalKind_legacy(cls, entity, softfail=False, **kwargs):
        
        from ProvidenceClarity.data.entity import E
        
        entity_class = entity.__class__
        
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

        try:
            k = entity.key()
        except:
            k = db.Key.from_path('E',1)
            
        
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
        ClassObj = type(entity.class_key()[-1], (Expando,), n_prop)

        natural_kind_record = ClassObj(key=_n_key, **kwargs)
        t_entity = entity_class(key=_e_key) ## create trimmed entity
        
        for prop in n_prop:
            setattr(natural_kind_record, prop, getattr(entity, prop))

            if prop in entity._entityIndexedProperties():
               setattr(t_entity, prop, getattr(entity, prop)) ## move indexed properties over to new Entity
        
        return t_entity, natural_kind_record
        
        

# Utility class for proto and dev structure
class DataManager(object):
    
    models = []
    entities = []
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
        
        from ProvidenceClarity.data.entity import E
        from ProvidenceClarity.api.data.transaction import TransactionController
        
        self.models = []
        self.entities = []
        
        if hasattr(self, 'base'):
            
            logging.info('Has base.')
            
            self.base()
            
            if isinstance(self.models, list):
                
                models_list = []
                entities_list = self.entities[:]
                
                for item in range(0, len(self.models)):
                    
                    if hasattr(self.models[item], '_PC_MODEL_BRANCH') and getattr(self.models[item], '_PC_MODEL_BRANCH') == _PC_MODEL_BRANCH_POLY:
                        entities_list.append(self.models[item])
                    else:
                        models_list.append(self.models[item])
                        
            else:
                return None
                
            if models_list is not None and isinstance(models_list, list) and len(models_list) > 0:

                mod = db.put(models_list)
            else:
                mod = None
                
            if entities_list is not None and isinstance(entities_list, list) and len(entities_list) > 0:
                ent = TransactionController.batchQueuedTransaction('entityCreate', entities_list)
        else:
            return True
    
    
_controller = DataController