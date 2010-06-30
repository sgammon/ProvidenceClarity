from google.appengine.ext import db

class Dev(object):
    
    def insert():
        pass
        
    def clean():
        pass
        
    def do_insert():
        models = self.insert()

        if isinstance(models, list):
            db.put(models)
                
            
    def do_clean():
        models = self.clean()
        
        if isinstance(models, list):
            db.delete(models)