import logging
from .. import RequestHandler
from google.appengine.ext import db
from ProvidenceClarity.data import data
from ProvidenceClarity.api.data import DataController
from ProvidenceClarity.api.index import IndexController
from ProvidenceClarity.api.cache import CacheController


class TransactionWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>transactionworker get</b>')
        
    def post(self):
        
        commit_list = {'puts':[],'deletes':[],'tasks':[]}
        
        logging.info('Prepping transaction worker...')
        
        if self.request.get('_tx_ticket', default_value=None) is not None:
            
            mode = self.request.get('_tx_worker', default_value='QueuedTransaction')
            worker = getattr(data, self.request.get('_tx_worker', default_value='EntityCreateTask'))
            
            logging.info('_tx_ticket: '+str(self.request.get('_tx_ticket')))
            
            ticket = worker.get_by_key_name(self.request.get('_tx_ticket'))
            if isinstance(ticket, list):
                ticket = ticket[0]

            logging.info('ticket key: '+str(self.request.get('_tx_ticket')))

            logging.info('Retrieved ticket. '+str(ticket))

            if ticket is not None:
                
                ## tag ticket as started
                mode = self.request.get('_tx_mode',default_value=None)
                
                logging.info('Beginning work with mode '+str(mode)+'...')
                
                try:
                    if mode == 'writeOperation':
                    
                        def txn(ticket):
                            commit_list['puts'] = ticket.subject
                            db.put(commit_list['puts'])
                    
                    elif mode == 'deleteOperation':
                    
                        def txn(ticket):
                            commit_list['deletes'] = ticket.subject
                            db.delete(commit_list['deletes'])
                    
                    elif mode == 'entityCreate':
                        
                        logging.info('Defining entityCreate txn...')
                    
                        def txn(ticket):
                            
                            logging.info('Beginning transaction.')
                            
                            entity, natural = DataController.generateNaturalKind(ticket.subject)
                            
                            logging.info('Split natural kind. N: '+str(natural)+', E: '+str(entity))
                            
                            if ticket.queue_indexing:

                                logging.info('Indexing requested. Queueing request...')

                                index_queue, index_task = IndexController.queueNewEntity(entity, return_task=True)
                                index_task.add(index_queue.name, transactional=True)
                                
                            if ticket.queue_caching:

                                logging.info('Caching requested. Queueing request...')
                                
                                cache_queue, cache_task = CacheController.queueNewEntity(entity, return_task=True)
                                cache_task.add(cache_queue.name, transactional=True)


                            ## @TODO: figure out way to merge descriptors in and put them too
                            
                            #if ticket.attachments is not None:
                            #    for item in ticket.attachments:
                            #        pass
                                    
                            logging.info('Putting commit list...')

                            return True
                    
                    elif mode == 'entityUpdate':
                    
                        def txn(ticket):
                            commit_list['puts'] = ticket.subject
                            db.put(commit_list['puts'])
                
                    elif mode == 'entityDelete':
                    
                        def txn(ticket): ## @TODO: Fill out procedures for entity delete besides deleting entire entity group
                            q = db.Query().ancestor(ticket.subject)
                            q.keys_only = True
                            c = q.count()
                            commit_list['deletes'] = q.fetch(c.count())
                            db.delete(commit_list['deletes'])
                    
                    elif mode == None:
                        ## @TODO: error handling
                        self.response.set_status(404)
                        self.render_raw('404 Fail: No Mode Given')
                    
                    else:
                        ## @TODO: error handling
                        self.response.set_status(404)
                        self.render_raw('404 Fail: Invalid Mode')
                        
                    logging.info('Ticket dump: '+str(ticket))
                    logging.info('Ticket properties: '+str(ticket.properties()))
                    db.run_in_transaction_custom_retries(3, txn, ticket)
                    logging.info('Transaction complete.')
                
                #except:
                #   ## @TODO: error handling
                #    logging.critical('Error 500 during transaction processing.')
                #    self.response.set_status(500)
                #    self.render_raw('<b>500 Error:</b> shit failed and blew up no idea why')

                finally:
                    ## @TODO: update ticket
                    ticket.status = 'complete'
                    ticket.put()
                    self.render_raw('<b>Transaction success</b>')
            
            else:
                ## @TODO: error handling
                logging.critical('Ticket not found.')
                self.response.set_status(404)
                self.render_raw('404 Ticket Invalid: Not Found (get_by_key_name returned None)')
        
        else:
            ## @TODO: error handling
            logging.critical('Ticket not provided.')
            self.response.set_status(404)
            self.render_raw('404 Ticket Invalid: Not Found')
            
        
class IndexWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>IndexWorker get</b>')
        
    def post(self):
        
        self.render_raw('<b>IndexWorker post</b>')
        
        
class CacheWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>CacheWorker get</b>')
        
    def post(self):
        
        self.render_raw('<b>CacheWorker post</b>')
        

class HygieneWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>HygieneWorker</b>')
        
    def post(self):
        
        self.render_raw('<b>HygieneWorker</b>')
        
        
class ExpirationWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>ExpirationWorker</b>')
        
    def post(self):
        
        self.render_raw('<b>ExpirationWorker</b>')

        
class SchedulerWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>SchedulerWorker</b>')

    def post(self):
        
        self.render_raw('<b>SchedulerWorker</b>')