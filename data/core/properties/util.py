from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors

from . import PCCustomProperty

BadValueError = datastore_errors.BadValueError
    
## +=+=+ Automatically decodes list members from UTF-8 and converts them to lower case.
class NormalizedStringListProperty(db.StringListProperty, PCCustomProperty):
    
    _storage_type_name = 'nstr_list'
    
    def validate_list_contents(self, value):
        final_list = []
        for item in value:
            
            if not isinstance(item, basestring):
                raise BadValueError('Items in the %s list must all be strings' % (self.name))
            else:
                final_list.append(str(item).decode('utf-8').lower())
        return final_list

## +=+=+ Serializes/deserializes list object on access instead of on fetch
class ListProperty(db.ListProperty):
    pass
    
## +=+=+ Automatically converts in and out of JSON objects from text properties.
class JSONProperty(db.TextProperty, PCCustomProperty):
    
    _storage_type_name = 'json'
    
    pass

## +=+=+ Automatically converts in and out of RDF objects from text properties.
class RDFProperty(db.TextProperty, PCCustomProperty):
    
    _storage_type_name = 'rdf'
    
    def get_value_for_datastore(self, model_instance):
        pass
    
    def make_value_from_datastore(self, value):
        pass