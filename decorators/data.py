import logging
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.data import data
from ProvidenceClarity.api.data import DataController
from ProvidenceClarity.api.data.transaction import TransactionController


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
def QueuedTransaction(mode, eta=None, decorators=None, retries=pc_config.get('default_retries','decorators.data.QueuedTransaction')):
        
    global _mode
    _mode = mode
    
    def _select_op(*args):
        
        global _mode
        
    
        worker = TransactionController.getTxnForDecorator(_mode)
        return worker
    
        
    return _select_op
    
    
