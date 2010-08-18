import logging
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.data import data
from ProvidenceClarity.api.data import DataController
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel

url_prefix = pc_config.get('pc_url_prefix','handlers','/_pc')


def NaturalKindFactory(fn):
    
    def data_put(models):

        _rpc = db.create_rpc(deadline=5, read_policy=db.EVENTUAL_CONSISTENCY)
    
        if isinstance(models, str):
            models = [models]
        
        puts_list = []
        for model in models:
            entity, natural = DataController.generateNaturalKind(model)
            puts_list.append(entity)
            if natural is not None: puts_list.append(natural)

        return fn(models, rpc=_rpc)

    return data_put
    
    
_mode = None
def QueuedTransaction(mode, eta=None, decorators=None, retries=pc_config.get('default_retries','decorators.data.QueuedTransaction'), worker_opts={}, task_opts={}, **kwargs):
        
    global _mode
    _mode = mode
    
    def _select_op(*args):
        
        global _mode
        def entity_create(*args):

            worker = data.EntityCreateTask
            models = args[0]
        
            import uuid
        
            if isinstance(models, Model):
                models = [models]

            task_objects = []
            task_records = []
        
            for entry in models:
                ticket = uuid.uuid4()
                task_records.append(worker(key_name=str(ticket),subject=entry,url=url_prefix+'/worker/data/transaction',attachments=decorators,eta=None,**task_opts))
                task_objects.append(taskqueue.Task(url=url_prefix+'/worker/data/transaction',params=dict({'_tx_mode':mode,'_tx_retries':retries,'_tx_eta':None,'_tx_ticket':str(ticket),'_tx_worker':'EntityCreateTask'}, **worker_opts)))
        
            def txn(task_records, task_objects):
                return ([x.add('transaction-queue', True) for x in task_objects], db.put(task_records))
        
            return db.run_in_transaction(txn, task_records, task_objects)
    
        if mode == 'entityCreate':
            return entity_create
    
        
    return _select_op
    
    
