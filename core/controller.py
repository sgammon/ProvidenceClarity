import exceptions
from . import PCCoreProxy, ProvidenceClarityObject
from ProvidenceClarity.api.util import import_helper


# Controls the loading and creation of PC Controllers
class ProvidenceClarityController(type):
    
    def __new__(meta, classname, bases, classDict):
        
        if '_subcontrollers' not in classDict:
            classDict['_subcontrollers'] = []
        if '_subcontroller_dispatch' not in classDict:
            classDict['_subcontroller_dispatch'] = {}
                            
        return type.__new__(meta, classname, bases, classDict)
        

# Proxies a PC controller into the platform object
class PCControllerProxy(PCCoreProxy):

    __metaclass__ = ProvidenceClarityController
    c_class = None

    def __init__(self, package_name, controller):
        
        if isinstance(controller, ProvidenceClarityController):
            self.c_class = controller()
            self.c_class.__api_package_name__ = package_name
        else:
            raise exceptions.InvalidController('Cannot proxy with non-compliant controller.') ## TODO: specific exception here
    
    def __get__(self, _instance, _class):
        return self.c_class
        
    def __set__(self, instance, value):
        raise NotImplemented
        
    def __delete__(self, instance):
        raise NotImplemented


# Master controller object
class PCController(ProvidenceClarityObject):

    __metaclass__ = ProvidenceClarityController
       
    def __getattr__(self, name):

        super_obj = super(PCController, self)

        if name in super(PCController, self).__getattribute__('_subcontrollers'):
            api_package_name = super_obj.__getattribute__('__api_package_name__')
            stack = ['ProvidenceClarity','api',api_package_name] + super(PCController, self).__getattribute__('_subcontrollers')[name]

            api_object, props = import_helper(stack[0:-1],stack[-1])
            
            self._subcontroller_dispatch[name] = PCControllerProxy(name, props['dict'][stack[-1]])
            return self._subcontroller_dispatch[name].__get__(self, super(PCController, self).__getattribute__('__class__'))
        else:
            return super_obj.__getattribute__(name)


# Master adapter object
class PCAdapter(ProvidenceClarityObject):

    def adapt(self, input=None):
        pass
            