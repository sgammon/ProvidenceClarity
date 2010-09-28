from .. import RequestHandler
from ProvidenceClarity.api.util import import_helper
from ProvidenceClarity.api.data import DataController
from ProvidenceClarity.api.data.stub import StubController
from ProvidenceClarity.api.input.receiver import ReceiverController


class ReceiverHandler(RequestHandler):


    def get(self, receiver_key=False):
        
        self.render_raw('<b>ReceiverHandler</b>') ## @TODO: Return a JSON struct describing this receiver
        

    def post(self, receiver_key=False):
        
        if receiver_key is not False:
            
            data = self.request.body

            if data is None:
                self.render_raw('Must provide some post content') # @TODO: Uniform exception/error formatting here
            else:
            
                ## Get receiver ticket
                r = ReceiverController.getAndValidate(receiver_key)
                
                ## Generate data stub & store data
                d_stub = StubController.create(r.default_data_backend, r.default_format, 'input', r)
                stubkey = StubController.store(d_stub)
                
                ## Resolve job template
                if r.default_job_template is not None:
                    pass ## LEFT OFF HERE WORKING ON JOB CONTROLLER

            
        else:
            self.render_raw('Must provide a receiver key') # @TODO: Integrated error/format handling like the Data API