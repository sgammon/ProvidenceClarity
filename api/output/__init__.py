from ProvidenceClarity import PCController, PCAdapter

    
class OutputController(PCController):

    _subcontrollers = {'grapher':['grapher','GraphController'],'viewer':['viewer','ViewController']}


class OutputAdapter(PCAdapter):
    pass    
    
_controller = OutputController