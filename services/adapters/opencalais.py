from string import Template
from ProvidenceClarity import pc_config
from . import ServiceAdapter

from google.appengine.ext import db

import simplejson as json

class OpenCalais(ServiceAdapter):

    # Service Adapter Properties
    adapter_name = 'opencalais'
    required_config = ['open_calais_key']
    calais_endpoint = 'http://api.opencalais.com/tag/rs/enrich'

    # Headers to include
    base_headers = {'x-calais-licenseID':None,
                    'content-type':None,
                    'accept':'application/json',
                    'calculateRelevanceScore':  'true',
                    'enableMetadataType':  'GenericRelations,SocialTags',
                    'docRDFaccessible':  'true',
                    'allowDistribution':  'false',
                    'allowSearch':  'false',
                    'submitter':  'Providence/Clarity INC'}
    
    
    @classmethod
    def _firstrun(cls):
        return self.service_adapter_d(key_name='opencalais',name='OpenCalais',description='Converts unstructured text into structured, linked entities.',
                                        homepage=db.Link('http://www.opencalais.com',docs=db.Link('http://www.opencalais.com/documentation/opencalais-documentation'))).put()

    def _init(self):
        return True

    def _issue_call(self, content, **kwargs):
        
        params = {}

        params['licenseID'] = self.config_properties['open_calais_key']
        params['content'] = content
        params['paramsXML'] = str(Template(self.params_template).substitute(**base_params)).strip().replace("\n",'')
        
        if len(kwargs) > 0:
            for param in kwargs:
                params[param] = kwargs[param]

        return self._fetch_url(calais_endpoint, params)
        
    def _process_response(self, response):

        status, content = response
        
        if status == 200:
            return json.loads(content)
        
    def _cleanup(self):
        return True