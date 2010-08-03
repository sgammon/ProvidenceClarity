import urllib
from google.appengine.api import urlfetch
from ProvidenceClarity.data.services import ServiceAdapter, ServiceRequest


class ServiceAdapter(object):

    # Service Adapter Properties
    required_config = []
    config_properties = {}

    # Data Models
    service_adapter_d = ServiceAdapter
    service_request_d = ServiceRequest
    
    # Cached Data Models
    adapter_model = None
    request_model = None
    
    # Request Caching
    last_request_status = None
    last_request_content = None

    ## Protoypes for Submethods
    def _init(self):
        return True

    def _issue_call(self, method, params={}):
        return None
        
    def _process_response(self, response):
        return None

    def _cleanup(self):
        return True
    
    @classmethod
    def _fetch_url(cls, url, params={}):

        result = urlfetch.fetch(url+urllib.urlencode(params))
        
        self.last_request_status = result.status_code
        self.last_request_content = result.content
        
        return (result.status_code, result.content)
        

    ## Front-end Methods
    @classmethod
    def do_call(cls, *args, **kwargs):
    
        # retrieve service adapter first, or firstboot
        adapter_model = cls.service_adapter_d.get_by_key_name(cls.adapter_name)
        if adapter_model is None:
            adapter_model = cls._firstboot()
    
        # perform any init stuff
        cls._init()
        
        # perform actual call & process response
        response = cls._process_response(cls._issue_call(*args, **kwargs))
        
        # do cleanup
        cls._cleanup()
        
        # return response
        return response