from .. import RequestHandler
from ProvidenceClarity.api.util import import_helper
from ProvidenceClarity.api.analyzer import AnalyzerController
from ProvidenceClarity.api.input.receiver import ReceiverController


class ReceiverHandler(RequestHandler):


    def get(self, receiver_key=False):
        
        self.render_raw('<b>ReceiverHandler</b>') ## @TODO: Return a JSON struct describing this receiver
        

    def post(self, receiver_key=False):
        
        if receiver_key is not False:
            
            data = self.request.get('content',default_value=None)
            if data is None:
                self.render_raw('Must provide some post content') # @TODO: Uniform exception/error formatting here
            else:
            
                r = ReceiverController.getAndValidate(receiver_key)
                if r.data_handler is not None:

                    m = import_helper(r.data_handler)
                    p_data = m.process_data(data) ## @TODO: More error handling
                
                    if r.discard_after_handler != True:
                        d_stub = r.store(p_data) ## @TODO: Fill out store methods
                
                else:
                    d_stub = r.store(data)
                
                if r.queue_analysis_job == True:
                    
                    if r.analysis_template is not None:
                        i_template = r.analysis_template
                    else:
                        i_template = None
                        
                    r = AnalyzerController.addJob(stub=d_stub,source='receiver',template=r.analysis_template)
            
        else:
            self.render_raw('Must provide a receiver key') # @TODO: Integrated error/format handling like the Data API