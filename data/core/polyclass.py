from google.appengine.ext import db


## +=+=+ Metaclass controlling the creation of Providence/Clarity polymodel objects.
class ProvidenceClarityPolyClass(db.PropertiedClass):

    def __init__(self, name, bases, dct):
    
        if name == 'PolyModel':
            super(ProvidenceClarityPolyClass, self).__init__(name, bases, dct, map_kind=False)
            return

        elif PolyModel in bases:
    
            if getattr(self, '__class_hierarchy__', None):
                raise db.ConfigurationError(('%s cannot derive from PolyModel as __class_hierarchy__ is already defined.') % self.__name__)

            self.__class_hierarchy__ = [self]
            self.__root_class__ = self

            super(ProvidenceClarityPolyClass, self).__init__(name, bases, dct)
    
        else:

            super(ProvidenceClarityPolyClass, self).__init__(name, bases, dct, map_kind=False)

            self.__class_hierarchy__ = [c for c in reversed(self.mro()) if issubclass(c, PolyModel) and c != PolyModel]

            if self.__class_hierarchy__[0] != self.__root_class__:
                raise db.ConfigurationError('%s cannot be derived from both root classes %s and %s' % (self.__name__,self.__class_hierarchy__[0].__name__,self.__root_class__.__name__))
            
            _class_map[self.class_key()] = self