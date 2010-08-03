import logging
from google.appengine.ext import db
from . import DataAPIHandler

from ProvidenceClarity.data import entity, proto, index, cache, descriptor, relationship


def get_type_q(typename):
    
    _type = str(typename).lower()
    
    if _type == 'entity':
        q = entity.E
        
    elif _type == 'proto':
        q = proto.P
        
    elif _type == 'index':
        q = index.I
        
    elif _type == 'cache':
        q = cache.C
        
    elif _type == 'descriptor':
        q = descriptor.D
        
    elif _type == 'relationship':
        q = relationship.R
        
    else:
        ## @TODO: Error handling here
        q = False
        
    return q
    

class MasterTypeListHandler(DataAPIHandler):
    
    def get(self):
        
        response = ['entity','proto','index','cache','descriptor','relationship']
        
        self.respond(response)
        
        
class MasterQueryHandler(DataAPIHandler):
    
    def get(self):
        
        _gql = self.request.get('gql',default_value=None)

        if _gql is not None:
            self.query['is_gql'] = True
            self.query['gql'] = _gql
                
            self.respond(q.fetch(limit=self.query['limit'], offset=self.query['offset']))
            
        else:
            self.errors.append({'error':'EMPTY_GQL','param':'GQL','msg':'The \'gql\' parameter must be non-empty.'})
            self.result = 'failure'
            
            self.respond()

        
        self.respond([])
        

class TypeListHandler(DataAPIHandler):
    
    def get(self, _type):
                            
        q = db.Query(get_type_q(_type), keys_only=self.query['keys_only']).fetch(limit=self.query['limit'], offset=self.query['offset'])
         
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
    

class QueryTypeHandler(DataAPIHandler):
    
    def get(self, _type):
        
        _gql = self.request.get('gql',default_value=None)

        if _gql is not None:
            self.query['is_gql'] = True
            self.query['gql'] = _gql
        
            if self.query['keys_only'] == True:
                prefix = 'SELECT __key__ FROM '
            else:
                prefix = 'SELECT * FROM '
        
        
            q = db.GqlQuery(prefix+str(get_type_q(_type).__name__)+' '+_gql)
            logging.info('QUERY: '+prefix+str(get_type_q(_type).__name__)+' '+_gql)
        
            self.respond(q.fetch(limit=self.query['limit'], offset=self.query['offset']))
            
        else:
            self.errors.append({'error':'EMPTY_GQL','param':'GQL','msg':'The \'gql\' parameter must be non-empty.'})
            self.result = 'failure'
            
            self.respond()
        
    
class CreateEntityHandler(DataAPIHandler):
    
    def post(self, key):
        pass