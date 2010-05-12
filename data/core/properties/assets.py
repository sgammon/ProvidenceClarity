from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors

BadValueError = datastore_errors.BadValueError

class DynamicImageProperty(db.StringProperty):    
    pass
    
class DynamicJSProperty(db.StringProperty):
    pass
    
class DynamicStyleProperty(db.StringProperty):
    pass

class DynamicBlobProperty(db.StringProperty):
    pass

class StaticFlashProperty(db.StringProperty):
    pass