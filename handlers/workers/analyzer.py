from .. import RequestHandler


class ObjectAnalyzer(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>ObjectAnalyzer</b>')

    def post(self):
        
        self.render_raw('<b>ObjectAnalyzer</b>')
        
        
class RelationAnalyzer(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>RelationAnalyzer</b>')
        
    def post(self):
        
        self.render_raw('<b>RelationAnalyzer</b>')
        
        
class StatAnalyzer(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>StatAnalyzer</b>')
        
    def post(self):
        
        self.render_raw('<b>StatAnalyzer</b>')
        
        
class MapReduceAnalyzer(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>MapReduceAnalyzer</b>')

    def post(self):
        
        self.render_raw('<b>MapReduceAnalyzer</b>')