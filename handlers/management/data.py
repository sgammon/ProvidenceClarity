from ProvidenceClarity.handlers import RequestHandler

class RootList(RequestHandler):
    
    def get(self):
        
        self.response_raw('<b>cool.</b>')
        
