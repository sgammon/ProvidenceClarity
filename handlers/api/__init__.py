from .. import RequestHandler

import logging, datetime
from ProvidenceClarity import pc_config
from ProvidenceClarity.lib import simplejson as json

class DataAPIHandler(RequestHandler):
    
    def package_data(self, data):

        if isinstance(data, list):
            res = []
            for item in data:
                res.append(self._process_object(item, False))
                
        else:
            res = self._process_object(data, False)
            
        return res


    def _process_object(self, object, fetch_proto=False):

        
        obj = {'key':str(object.key()),'kind':object.kind(),'properties':{}}

        if object.key().has_id_or_name():
            obj['key'] = (str(object.key()), object.key().id_or_name())
            
        if hasattr(object, pc_config.get('poly_class_field','data','_class_key_')):
            obj['class'] = '.'.join(getattr(object, pc_config.get('poly_class_field','data','_class_key_')))
            
        for key, value in object.properties().items():
            
            if value.__class__.__name__ == 'ReferenceProperty':
                continue
                
            obj['properties'][key] = {'type':value.__class__.__name__, 'value':str(getattr(object, key))}
            
        return obj

    
    def respond(self, data):
        
        format = self.request.get('out',default_value='json')
        
        response_obj = {'result':'success', 'content_type':None, 'content':self.package_data(data)}
        
        if isinstance(data, list):
            response_obj['content_type'] = 'list'
        else:
            response_obj['content_type'] = 'item'
        
        if format == 'json':
            response = json.dumps(response_obj)
            
        elif format == 'xml':
            response = str(response_obj) ## TODO: ADD XML ENCONDING

        self.render_raw(str(response))