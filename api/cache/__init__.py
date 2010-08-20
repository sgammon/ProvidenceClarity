import logging, datetime
from google.appengine.ext import db
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.main import PCController
from ProvidenceClarity.api.data import DataController

from ProvidenceClarity.data.cache import NormalizedObject

url_prefix = pc_config.get('pc_url_prefix','handlers','/_pc')


class CacheController(PCController):
    
    @classmethod
    def _model_from_protobuf(cls, pb, _entity_class=datastore.Entity):
        
        logging.info('=========== Model from Protobuf ===========')
        logging.info('Pb: '+str(pb))
        
        entity = _entity_class.FromPb(pb)
        
        logging.info('Entity: '+str(entity))

        _n_obj = NormalizedObject.from_entity(entity)

        if _n_obj.data_class_path is not None:

            classpath = _n_obj.data_class_path.split('.')
            model = DataController.import_model(classpath)
            
            logging.info('Model: '+str(model))
        else:
            logging.critical('No data class path pointer found.') ##@TODO: fallback to regular from entity

        if _n_obj.key().parent() is not None:
            if _n_obj.key().name() is not None:
                obj = model(_n_obj.key().parent(),key_name=_n_obj.key().name())
            else:
                obj = model(_n_obj.key().parent())
        else:
            if _n_obj.key().name() is not None:
                obj = model(key_name=_n_obj.key().name())
            else:
                obj = model()

        for item in entity:
            logging.info('Setting model property '+str(item) +' to value '+str(entity[item]))
            setattr(obj, item, entity[item])
        
        #res = model.from_entity(entity)
        logging.info('Finishing up and returning '+str(obj)+'.')
        return obj

    @classmethod
    def _model_to_protobuf(cls, model_instance, _entity_class=datastore.Entity):
        
        logging.info('=========== Model to Protobuf ===========')
        logging.info('Model: '+str(model_instance))
        
        if model_instance.key().parent() is not None:
            
            logging.info('Model has parent.')
            
            if model_instance.key().name() is not None:
                
                logging.info('Model has key name.')
                
                n = NormalizedObject(model_instance.key().parent(), key_name=model_instance.key().name())
            else:
                
                logging.info('Model has no key name.')
                n = NormalizedObject(model_instance.key().parent())
        else:
            logging.info('Model has no parent.')
            
            if model_instance.key().name() is not None:
                logging.info('Model has key name.')
                n = NormalizedObject(key_name=model_instance.key().name())
            else:
                logging.info('Model has no key name.')
                n = NormalizedObject()
            
        logging.info('nE: '+str(n))        
        logging.info('Copying model properties...')
        
        _props = model_instance.properties()
        _d_props = model_instance.dynamic_properties()
        
        for prop in list(_props.keys()+_d_props):
            
            value = getattr(model_instance, prop)

            if isinstance(value, list) and len(value) == 0:
                continue
            else:    
                setattr(n, prop, getattr(model_instance, prop))

            logging.info('Setting prop '+str(prop)+' to '+str(getattr(model_instance, prop)))
                
        logging.info('Setting model path property as '+str(model_instance.class_key())+'...')
        
        n.data_class_path = '.'.join(model_instance.path_key())
                
        _mi = n._populate_entity(_entity_class).ToPb()
        logging.info('_N: '+str(_mi))
                
        return _mi
    
    @classmethod
    def to_protobuf(cls, input):
        
        if input is None:
            return None

        elif isinstance(input, db.Model):
            return cls._model_to_protobuf(input).Encode()

        elif isinstance(input, list):
            return [cls._model_to_protobuf(x).Encode() for x in input]
        
    @classmethod
    def from_protobuf(cls, protobuf):
        
        if protobuf is None:
            return None

        elif isinstance(protobuf, str):
            return cls._model_from_protobuf(entity_pb.EntityProto(protobuf))
            
        elif isinstance(protobuf, list):
            return [cls._model_from_protobuf(entity_pb.EntityProto(x)) for x in protobuf]
            
    @classmethod
    def queueNewEntity(cls, entity, return_task=False, task_opts={}):
        
        if isinstance(entity, db.Model):
            entity = entity.key()
        elif isinstance(entity, db.Key):
            pass
        else:
            return False
        
        task_params = {'operation':'cache_by_key','key':str(entity),'url':url_prefix+'/workers/data/cacher'}
        for item in task_opts:
            task_params[item] = task_opts[item]
        
        q = taskqueue.Queue(name='cacher')
        t = taskqueue.Task(name=str(entity),params=task_params)
        if return_task == True:
            return (q, t)
        else:
            return q.add(t)