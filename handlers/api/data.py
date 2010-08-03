from . import DataAPIHandler

from ProvidenceClarity.data import entity, proto, index, cache, descriptor, relationship


class MasterTypeListHandler(DataAPIHandler):
    
    def get(self):
        
        response = ['entity','proto','index','cache','descriptor','relationship']
        
        self.respond(response)
        

class TypeListHandler(DataAPIHandler):
    
    def get(self, _type):
        
        _type = str(_type).lower()
        
        i_limit = int(self.request.get('limit',default_value='20'))
        i_offset = int(self.request.get('offset',default_value='0'))
        
        if _type == 'entity':
            q = entity.E.all().fetch(limit=i_limit, offset=i_offset)
            
        elif _type == 'proto':
            q = proto.P.all().fetch(limit=i_limit, offset=i_offset)
            
        elif _type == 'index':
            q = index.I.all().fetch(limit=i_limit, offset=i_offset)
            
        elif _type == 'cache':
            q = cache.C.all().fetch(limit=i_limit, offset=i_offset)
            
        elif _type == 'descriptor':
            q = descriptor.D.all().fetch(limit=i_limit, offset=i_offset)
            
        elif _type == 'relationship':
            q = relationship.R.all().fetch(limit=i_limit, offset=i_offset)
            
         
        self.respond(q)
        

class GetHandler(DataAPIHandler):
    
    def get(self, key):
        pass
    
    
class DeleteHandler(DataAPIHandler):
    
    def get(self, key):
        pass
    
    
class UpdateHandler(DataAPIHandler):
    
    def post(self, key):
        pass
    
    
class CreateTypeHandler(DataAPIHandler):
    
    def post(self, key):
        pass
    
    
class CreateEntityHandler(DataAPIHandler):
    
    def post(self, key):
        pass