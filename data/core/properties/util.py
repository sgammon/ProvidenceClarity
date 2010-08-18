import logging
from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors

from ProvidenceClarity.api.cache import CacheController

from . import PCCustomProperty

BadValueError = datastore_errors.BadValueError


def force_encode_utf8(string):
    if type(string) == 'str':
        return string
    else:
        return string.encode('utf-8')
        
def force_decode_utf8(string):
    if type(string) == unicode:
        return string
    return string.decode('utf-8')


# +=+=+ Stores a pickled (cached) copy of a Python object
class CachedObject(db.Property, PCCustomProperty):

    data_type = db.Blob
    _storage_type_name = 'cached_obj'

    def get_value_for_datastore(self, model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        if value is not None:
            return db.Blob(pickle.dumps(value))

    def make_value_from_datastore(self, value):
        if value is not None:
            return pickle.loads(value)
            
# +=+=+ Stores a list of pickled (cached) Python objects
class CachedObjectList(db.ListProperty, PCCustomProperty):
    
    data_type = db.Blob
    _storage_type_name = 'cached_obj_list'
    
    def __init__(self, *args, **kwargs):
        super(CachedObjectList, self).__init__(self.data_type, *args, **kwargs)
    
    def get_value_for_datastore(self, model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        if value is not None:
            return [db.Blob(pickle.dumps(x)) for x in value]

           
# +=+=+ Stores a protobuf copy of a system datastore entity
class CachedProtobuf(db.Property, PCCustomProperty):
    
    data_type = db.Blob
    _storage_type_name = 'cached_pb'
    
    def __init__(self, *args, **kwargs):
        kwargs['indexed'] = False
        super(CachedProtobuf, self).__init__(*args, **kwargs)
    
    def get_value_for_datastore(self, model_instance):
        logging.info('GET VALUE FOR DATASTORE.')
        value = self.__get__(model_instance, model_instance.__class__)
        if value is not None:
            pb_s = CacheController.to_protobuf(value)
            logging.info('Protobuf: '+str(pb_s))
            logging.info('Storing value (following this log)')
            #_pb = force_encode_utf8(pb_s)
            return db.Blob(pb_s)
            
    def make_value_from_datastore(self, value):
        logging.info('MAKE FROM DATASTORE')
        logging.info('Value: '+str(value))
        if value is not None:
            logging.info('Retrieving value (following this log)')
            logging.info(str(CacheController.from_protobuf(value)))
            return CacheController.from_protobuf(value)


# +=+=+ Stores a list of protobuf copies of related system datastore entities
class CachedProtobufList(db.ListProperty, PCCustomProperty):
    
    data_type = db.Blob
    _storage_type_name = 'cached_multi_pb'
    
    def __init__(self, *args, **kwargs):
        
        kwargs['indexed'] = False
        super(CachedProtobufList, self).__init__(self.data_type, *args, **kwargs)

    def validate(self, value):
        if isinstance(value, list) == False:
            raise BadValueError('Must be given a list of entities to protobuf.')
        if value is not None:
            value = self.validate_list_contents(value)
        return value
    
    def validate_list_contents(self, value):
        return [db.Blob(CacheController.to_protobuf(x)) for x in value]
    
    def make_value_from_datastore(self, value):
        return [CacheController.from_protobuf(x) for x in value]
        
    
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