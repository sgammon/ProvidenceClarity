import datetime, exceptions
from . import PCCoreProxy

from google.appengine.api import quota

# Clock object measures timepoints for debugging/etc.
class PCClockProxy(PCCoreProxy):
    
    _clock = []
    
    def __init__(self):
        self.timepoint('boot')
            
    def timepoint(self, name):
        time_value = datetime.datetime.now()
        self._clock.append((name, {'time':time_value, 'cpu':quota.get_request_cpu_usage(), 'cpu_api':quota.get_request_api_cpu_usage()}))
        return True
        
    def dump(self):
        return _clock      
