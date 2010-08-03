from .. import RequestHandler

class Error404(RequestHandler):

    """ Template: util/Error404.html """
    
    def get(self):
        
        self.render('util/Error404.html',page={'title':'404 Not Found'})
    

class Error403(RequestHandler):
    
    """ Template: util/Error403.html """
    
    def get(self):
        
        self.render('util/Error403.html',page={'title':'403 Forbidden'})