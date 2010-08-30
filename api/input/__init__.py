from .. import AdapterInterface
from ProvidenceClarity import PCController


class InputAdapter(AdapterInterface):
    pass
    
    
class InputController(PCController):

    _subcontrollers = {'receiver':['receiver','ReceiverController'],'scraper':['scraper','ScraperController']}
    
    
_controller = InputController