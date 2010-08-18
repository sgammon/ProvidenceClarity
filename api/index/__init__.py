from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.main import PCController

## get url

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
        t = taskqueue.Task(name=str(entity),params={'operation':'index_by_key','key':str(entity)},url=url_prefix+'/workers/data/indexer',**task_opts)
        if return_task == True:
            return (q, t)
        else:
            return q.add(t)