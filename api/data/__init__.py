__all__ = ['cacher','indexer','proto']

import logging
from google.appengine.ext import db, blobstore
from ProvidenceClarity.main import PCController

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
    pass
    

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
    