from .. import RequestHandler


class HygieneWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>HygieneWorker</b>')
        
    def post(self):
        
        self.render_raw('<b>HygieneWorker</b>')
        
        
class ExpirationWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>ExpirationWorker</b>')
        
    def post(self):
        
        self.render_raw('<b>ExpirationWorker</b>')

        
class SchedulerWorker(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>SchedulerWorker</b>')

    def post(self):
        
        self.render_raw('<b>SchedulerWorker</b>')