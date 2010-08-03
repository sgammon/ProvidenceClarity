from string import Template
from ProvidenceClarity import pc_config
from . import ServiceAdapter

from google.appengine.ext import db

import simplejson as json

class OpenCalais(ServiceAdapter):

    # Service Adapter Properties
    adapter_name = 'opencalais'
    required_config = ['open_calais_key']
    calais_endpoint = 'http://api.opencalais.com/enlighten/rest/'
    
    # Default Parameters to Include
    base_params =  {'outputFormat':  'Application/JSON',
                    'calculateRelevanceScore':  'true',
                    'enableMetadataType':  'GenericRelations,SocialTags',
                    'docRDFaccessible':  'false',
                    'allowDistribution':  'false',
                    'allowSearch':  'false',
                    'submitter':  'Providence/Clarity INC'}
                    
    params_template = '''

    <c:params xmlns:c="http://s.opencalais.com/1/pred/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    
        <c:processingDirectives c:contentType="$contentType" c:enableMetadataType="$enableMetadataType" c:outputFormat="$outputFormat" c:docRDFaccesible="$docRDFaccessible" >
        </c:processingDirectives>

        <c:userDirectives c:allowDistribution="$allowDistribution" c:allowSearch="$allowSearch" c:externalID="$externalID" c:submitter="$submitter">
        </c:userDirectives>

        <c:externalMetadata>
        </c:externalMetadata>
    
    </c:params>

    '''

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