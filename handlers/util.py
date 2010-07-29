from . import RequestHandler


class IndexHandler(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>Index!</b>')
    

class Error404(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>Error 404!</b>')
    

class Error403(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>Error 403!</b>')