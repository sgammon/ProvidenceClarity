from ProvidenceClarity import PCController, PCAdapter


class InputAdapter(PCAdapter):
    pass
    
    
class InputController(PCController):

    _subcontrollers = {'receiver':['receiver','ReceiverController'],'fetcher':['fetcher','FetchController']}
    
    
_controller = InputController