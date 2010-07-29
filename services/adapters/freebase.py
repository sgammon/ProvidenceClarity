from . import ServiceAdapter

class Freebase(ServiceAdapter):

    # Service Adapter Properties
    adapter_name = 'freebase'
    required_config = []

    def _firstrun(self):
        return self.service_adapter_d(key_name='freebase',name='Freebase',description='Disambiguates and links provided unstructured entities.',
                                        homepage=db.Link('http://www.freebase.com',docs=db.Link('http://wiki.freebase.com/wiki/Main_Page'))).put()
        
    def _init(self):
        return True

    def _issue_call(self, method, params={}):
        pass
        
    def _process_response(self, response):
        pass
        
    def _cleanup(self):
        pass