from ProvidenceClarity import PCController


class DevController(PCController):

    _subcontrollers = {'firstrun':['firstrun','FirstRunController']}
    
    
_controller = DevController