from google.appengine.ext import webapp


class IncomingXMPP(webapp.RequestHandler):
    
    def get(self):
        
        self.response.out.write('<b>IncomingXMPP</b>')
        
    def post(self):
        
        self.render_raw('<b>IncomingXMPP</b>')
        

class OutgoingXMPP(webapp.RequestHandler):
    
    def get(self):
        
        self.response.out.write('<b>OutgoingXMPP</b>')
        
    def post(self):
        
        self.render_raw('<b>OutgoingXMPP</b>')