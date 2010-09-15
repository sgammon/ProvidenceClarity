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
            
                r = ReceiverController.getAndValidate(receiver_key)
                d_stub = StubController.get
                
                d_stub = ReceiverController.get_stub(p_data,r) ## @TODO: Fill out store methods <--- CHECK
                stubkey = StubController.store(d_stub)
                
                else:
                    r = ReceiverController.getAndValidate(receiver_key)
                    d_stub = ReceiverController.get_stub(data,r)
                    StubController.store(d_stub)
                
                if r.queue_analysis_job == True:
                    
                    if r.analysis_template is not None:
                        i_template = r.analysis_template
                    else:
                        i_template = None
                    
                    ## todo
                    r = AnalyzerController.addJob(stub=d_stub,source='receiver',template=r.analysis_template)
            
        else:
            self.render_raw('Must provide a receiver key') # @TODO: Integrated error/format handling like the Data API