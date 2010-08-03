import logging
from google.appengine.ext import webapp
#from . import RequestHandler

RequestHandler = webapp.RequestHandler

class IndexHandler(RequestHandler):
    
    def get(self):
        
        #self.render_raw('<b>Index!</b>')
        self.response.out.write('<b>Index!</b>')