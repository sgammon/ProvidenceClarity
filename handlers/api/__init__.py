from google.appengine.ext import db
from .. import RequestHandler

import logging, datetime
from ProvidenceClarity import pc_config
from ProvidenceClarity.lib import simplejson as json

class DataAPIHandler(RequestHandler):
    
    query = {'limit':20, 'offset':0, 'keys_only':False, 'is_gql':False, 'gql':None}
    result = 'success'
    errors = []
    
    def initialize(self, request, response):
        
        try:
            self.query['limit'] = int(request.get('limit',default_value='20'))
        except ValueError:
            self.query['limit'] = 20
            self.errors.append({'error':'INVALID_PARAM','param':'LIMIT','msg':'The \'limit\' parameter must be an integer.'})
            
        try:
            self.query['offset'] = int(request.get('offset',default_value='0'))
        except ValueError:
            self.query['offset'] = 0
            self.errors.append({'error':'INVALID_PARAM','param':'OFFSET','msg':'The \'offset\' parameter must be an integer.'})
            
        self.query['keys_only'] = str(request.get('keys_only',default_value=False)).lower()
        
        if self.query['keys_only'] != False:
            if self.query['keys_only'] == '0':
                self.query['keys_only'] = False
            elif self.query['keys_only'] == '1':
                self.query['keys_only'] = True
            
            elif self.query['keys_only'] == 'true':
                self.query['keys_only'] = True
            elif self.query['keys_only'] == 'false':
                self.query['keys_only'] = False
            else:
                self.errors.append({'error':'INVALID_PARAM','param':'KEYS_ONLY','msg':'The \'keys_only\' parameter only accepts 1, 0, true, or false.'})
        
        super(DataAPIHandler, self).initialize(request, response)
        
    
    def package_data(self, data):

        if isinstance(data, list):
            res = []
            for item in data:
                res.append(self._process_object(item, False))
                
        else:
            res = self._process_object(data, False)
            
        return res


    def _process_object(self, object, fetch_proto=False):

        if isinstance(object, db.Model):
            
            obj = {'key':str(object.key()),'type':'model','kind':object.kind(),'app':object.key().app(),'parent':object.key().parent(),'properties':{}}

            if object.key().has_id_or_name():
                obj['key'] = (str(object.key()), object.key().id_or_name())
            
            if hasattr(object, pc_config.get('poly_class_field','data','_class_key_')):
                obj['class'] = '.'.join(getattr(object, pc_config.get('poly_class_field','data','_class_key_')))
            
            for key, value in object.properties().items():
            
                if value.__class__.__name__ == 'ReferenceProperty':
                    continue
                
                obj['properties'][key] = {'type':value.__class__.__name__, 'value':str(getattr(object, key))}
            
                return obj
                
        elif isinstance(object, db.Key):
                            
            obj = {'key':str(object),'type':'key','kind':object.kind(),'app':object.app(),'parent':object.parent()}
            
            if object.has_id_or_name():
                obj['key'] = (str(object), object.id_or_name())
                
            return obj

    
    def respond(self, data=None):
        
        format = self.request.get('out',default_value='json')
        caching = self.request.get('caching', default_value='json')
        
        if data is not None: data = self.package_data(data)
        
        response_obj = {'result':self.result, 'errors':self.errors, 'query':self.query, 'content_type':None, 'content': data}
        
        if data == None:
            response_obj['content_type'] = 'empty'
            response_obj['count'] = 0
        
        if isinstance(data, list):
            response_obj['content_type'] = 'list'
            response_obj['count'] = len(data)
        else:
            response_obj['content_type'] = 'item'
            response_obj['count'] = 1
        
        if format == 'json':
            response = json.dumps(response_obj)
            
        elif format == 'xml':
            response = str(response_obj) ## TODO: ADD XML ENCONDING

        self.render_raw(str(response))