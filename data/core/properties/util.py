from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors

BadValueError = datastore_errors.BadValueError
    
## +=+=+ Automatically decodes list members from UTF-8 and converts them to lower case.
class NormalizedStringListProperty(db.StringListProperty):
    
    def validate_list_contents(self, value):
        final_list = []
        for item in value:
            
            if not isinstance(item, basestring):
                raise BadValueError('Items in the %s list must all be strings' % (self.name))
            else:
                final_list.append(str(item).decode('utf-8').lower())
        return final_list

## +=+=+ Automatically converts in and out of RDF objects from text properties.
class RDFProperty(db.TextProperty):
    
    def get_value_for_datastore(self, model_instance):
        pass
    
    def make_value_for_datastore(self, value):
        pass