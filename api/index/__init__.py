from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.main import PCController

url_prefix = pc_config.get('pc_url_prefix','handlers','/_pc')

class IndexController(PCController):
                
    @classmethod
    def queueNewEntity(cls, entity, return_task=False, task_opts={}):
        
        if isinstance(entity, db.Model):
            entity = entity.key()
        elif isinstance(entity, db.Key):
            pass
        else:
            return False
        
        q = taskqueue.Queue(name='indexer')
        t = taskqueue.Task(params={'operation':'index_by_key','key':str(entity)},url=url_prefix+'/workers/data/indexer',**task_opts)
        if return_task == True:
            return (q, t)
        else:
            return q.add(t)