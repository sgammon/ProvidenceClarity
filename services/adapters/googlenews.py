from . import ServiceAdapter

class GoogleNews(ServiceAdapter):

    # Service Adapter Properties
    adapter_name = 'googlenews'
    required_config = ['google_ajax_key']

    def _firstrun(self):
        return self.service_adapter_d(key_name='googlenews',name='Google News',description='Retrieves news articles matching a query string.',
                                        homepage=db.Link('http://news.google.com',docs=db.Link('http://code.google.com/apis/ajaxsearch/documentation/'))).put()

    def _init(self):
        return True

    def _issue_call(self, method, params={}):
        pass
        
    def _process_response(self, response):
        pass

    def _cleanup(self):
        pass