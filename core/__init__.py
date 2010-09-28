

# Master ancestor class for all P/C-related classes
class ProvidenceClarityObject(object):
    pass


# Bridges a 'platform' property over to other objects
class PCPlatformBridge(object):
    
    platform = None
    
    def _setPlatformParent(self, platform):
        super(PCPlatformBridge, self).__setattr__('platform', platform)


# Parent to all platform proxy objects
class PCCoreProxy(ProvidenceClarityObject, PCPlatformBridge):
    
    def __repr__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __str__(self):
        return '<CoreProxy "'+str(self.__class__.__name__)+'">'
        
    def __unicode__(self):
        return u'<CoreProxy "'+str(self.__class__.__name__)+'">'