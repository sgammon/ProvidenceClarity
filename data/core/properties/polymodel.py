from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors

from ProvidenceClarity import pc_config

_PATH_PREFIX = pc_config.get('path_prefix','data',False)
_IMPORT_PREFIX = pc_config.get('import_prefix','data',False)

## +=+=+ Stores the Python package import path from the application root, for lazy-load on search.
class _ModelPathProperty(db.StringProperty):
    
    def __init__(self, name, **kwargs):
        super(_ModelPathProperty, self).__init__(name=name, default=None, **kwargs)

    def __set__(self, *args):
        raise db.DerivedPropertyError('Model-path is a derived property and cannot be set.')

    def __get__(self, model_instance, model_class):
        if model_instance is None: return self
        # @TODO: make seperator customizable from some import/config
        return ':'.join([i for i in str(model_instance.__module__+'.'+model_instance.__class__.__name__).split('.')])

## +=+=+ Stores the polymodel class inheritance path.
class _ClassKeyProperty(db.ListProperty):

    def __init__(self, name):
        super(_ClassKeyProperty, self).__init__(name=name,item_type=str,default=None)

    def __set__(self, *args):
        raise db.DerivedPropertyError('Class-key is a derived property and cannot be set.')

    def __get__(self, model_instance, model_class):
        if model_instance is None: return self
        return [cls.__name__ for cls in model_class.__class_hierarchy__]