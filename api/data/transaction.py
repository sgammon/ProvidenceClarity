import logging
from . import DataController

from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from ProvidenceClarity import pc_config
from ProvidenceClarity.data import data
from ProvidenceClarity.data.core.model import Model

url_prefix = pc_config.get('pc_url_prefix','handlers','/_pc')

execute_worker = False

### Define workers first

def entityCreate(*args):

    global execute_worker

    logging.info('args: '+str(args))

    worker = data.EntityCreateTask
    models = args[0]

    import uuid

    if isinstance(models, Model):
        models = [models]

    task_objects = []
    task_records = []
    
    decorators = None ## @TODO: Implement descriptors

    queue = data.TaskQueue.get_by_key_name('transaction-queue')

    for entry in models:
        ticket = uuid.uuid4()

        w = worker(key_name=str(ticket),queue=queue,subject=entry,url=url_prefix+'/worker/data/transaction',eta=None,attachments=decorators)
        t = taskqueue.Task(url=url_prefix+'/worker/data/transaction',params=dict({'_tx_mode':'entityCreate','_tx_retries':w.retries,'_tx_eta':None,'_tx_ticket':str(ticket),'_tx_worker':'EntityCreateTask'}))

        task_records.append(w)
        task_objects.append(t)

    def txn(task_records, task_objects, tasks_transactional=False):
        return ([x.add('transaction-queue', tasks_transactional) for x in task_objects], db.put(task_records))

    if execute_worker:

        if len(task_objects) > 5:
            tasks_transactional = False
        else:
            tasks_transactional = True

        return db.run_in_transaction(txn,task_records,task_objects,tasks_transactional)
    else:
        return txn, task_records, task_objects
        
        
workers = {'entityCreate':entityCreate}


### Transaction Controller            
class TransactionController(DataController):

    @classmethod
    def batchQueuedTransaction(cls,mode,input):
        
        logging.info('========== BATCH QUEUED TRANSATION ==========')
        logging.info('Mode: '+str(mode))
        logging.info('Input: '+str(input))
        
        if isinstance(input, list):
            
            logging.info('Input is list.')
            
            commit = {'txn':[],'records':[],'objects':[]}
            
            logging.info('Getting transaction objects...')
            
            
            txn, task_records, task_objects = cls.getTxn(mode, input)
            
            logging.info('Txn result: '+str(txn))
            logging.info('Records result: '+str(task_records))
            logging.info('Objects result: '+str(task_objects))
            
            q = taskqueue.Queue(name='transaction-queue')
            
            
            return (q.add(task_objects), db.put(task_records))
            
        else:
            return False ## @TODO: Error handling here
    
    
    @classmethod
    def getTxn(cls, mode, *args):
        
        global execute_worker

        if mode in workers:
            
            execute_worker = False
            return workers[mode](*args)
                

    @classmethod
    def getTxnForDecorator(cls, mode):
        
        global execute_worker

        if mode in workers:
            
            execute_worker = True
            return workers[mode]
