import exceptions
from . import PCCoreProxy


# Platform to store state information and key=>values for later use        
_state_object = {}
class PCStateProxy(PCCoreProxy):
        
    def __init__(self, state=None):
        global _state_object
        if state is not None:
            if isinstance(state, dict):
                for item in state:
                    _state_object[item] = state[item]
            
    def __getattr__(self, name):
        global _state_object
        if isinstance(_state_object, dict):
            if name in _state_object:
                return _state_object[name]
                    
    def __setattr__(self, name, value):
        global _state_object
        if isinstance(_state_object, dict):
            _state_object[name] = value
        else:
            _state_object = {name:value}
        
    def set(self, name, value):
        global _state_object
        if isinstance(_state_object, dict):
            _state_object[name] = value
            
    def get(self, name):
        global _state_object
        if isinstance(_state_object, dict):
            if name in _state_object:
                return _state_object[name]
            else:
                return None
        else:
            return None