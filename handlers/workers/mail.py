from .. import RequestHandler


class IncomingMail(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>IncomingMail</b>')
        
    def post(self):
        
        self.render_raw('<b>IncomingMail</b>')        


class OutgoingMail(RequestHandler):
    
    def get(self):
        
        self.response.out.write('<b>OutgoingMail</b>')
        
    def post(self):
        
        self.render_raw('<b>OutgoingMail</b>')        