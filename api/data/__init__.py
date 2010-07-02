import logging
from google.appengine.ext import db

class DataManager(object):
    
    models = []
    P = None
    
    def __init__(self):
        from ProvidenceClarity.data.proto import P
        self.P = P
    
    def do_test(self):
        logging.info('MANAGER: TEST COMPLETE!')
    
    ## passed down to child classes
    def insert(self):
        pass
    
    ## passed down to child classes
    def clean(self):
        pass
        
    def sanitize(self, data):
        
        if isinstance(data, list):
            
            index = data[:]
            
            for model in index:
                if model is None:
                    data.remove(model)
                    
            return data
        
        else:
            return False ## graceful fail
                
        
    def do_insert(self):
        
        self.models = []
        self.models = self.insert()

        if isinstance(self.models, list):
            
            try:
                res = db.put(self.sanitize(self.models))
                
            except:
                return False
                
            return (True,res)
                
            
    def do_clean(self):

        self.models = []
        self.models = self.clean()
        
        
        if isinstance(self.models, list):
            
            try:
                res = db.delete(self.sanitize(self.models))
            
            except:
                return False
                
            return (True,res)