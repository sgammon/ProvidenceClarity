import exceptions
from . import PCCoreProxy


# Proxies requests for config items (mainly done for consistency with other platform proxies)
class PCConfigProxy(PCCoreProxy):

    _c_module = None # Stores reference to pc_config module
    _c_data = None # Stores copy of config data for later switch to using this class (@TODO: Switch to universal config )

    def setConfig(self, config):
        self._c_module = config
        self._c_data = config.config
    
    def get(self, key, module, default=None):
        return self._c_module.get(key, module, default)
        
    def dump(self):
        return self._c_module.dump()
