from ProvidenceClarity.handlers import RequestHandler

class ViewerIndex(RequestHandler):
    
    """ Template: data/viewer_index.html """
    
    def get(self):
        
        self.response_raw('<b>coming soon</b>')
        
        
class DataCommit(RequestHandler):
    
    """ Simple redirects after data commit. """
    
    def post(self):
        
        pass
        
        
class DataList(RequestHandler):
    
    """ Template: data/list.html """
    
    def get(self):
        pass
        
        
class DataViewer(RequestHandler):
    
    """ Template: data/viewer.html """
    
    def get(self):
        pass