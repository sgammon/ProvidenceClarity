import logging
from google.appengine.ext import db
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.main import PCController
from ProvidenceClarity.api.data import DataController

url_prefix = pc_config.get('pc_url_prefix','handlers','/_pc')

class CacheController(PCController):
    
    @classmethod
    def _model_from_protobuf(cls, pb, _entity_class=datastore.Entity):
        
        entity = _entity_class.FromPb(pb)
        logging.info(str(entity))
        return class_for_kind(entity.kind()).from_entity(entity)

    @classmethod
    def _model_to_protobuf(cls, model_instance, _entity_class=datastore.Entity):
        
        setattr(model_instance, 'PC_CACHED_PATH', db.StringProperty())
        setattr(model_instance, 'PC_CACHED_PATH', model_instance._getModelPath())
        
        logging.info('GIVEN MODEL: '+str(getattr(model_instance, 'PC_CACHED_PATH')))
        logging.info('GIVEN MODEL: '+str(model_instance.properties()))
        
        _mi = model_instance._populate_entity(_entity_class).ToPb()
        logging.info('_MI: '+str(_mi))        
                
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