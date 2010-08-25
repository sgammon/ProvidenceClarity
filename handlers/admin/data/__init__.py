from ... import RequestHandler


class DataIndex(RequestHandler):
    
    """ Template:  """
    
    def get(self):
        
        self.render_raw('<b>DataIndex</b>')
        
        
class DataList(RequestHandler):
    
    def get(self):
        
        self.render_raw('<b>HTML Output</b>')
   
   
class DataCreate(RequestHandler):
    
    def get(self):
        
        pass
        
    def post(self):
        
        pass       
  
  
class DataView(RequestHandler):
    
    def get(self, type=False, key=False):
        
        self.render_raw('<b>Type: </b>'+str(type)+'<br /><b>Key: </b>'+str(key))


class DataEdit(RequestHandler):
    
    def get(self):
        
        pass

    def post(self):
        
        pass


class DataDelete(RequestHandler):
    
    def get(self):
        
        pass
        
    def post(self):
        
        pass