import logging, os, sys
from google.appengine.ext import db
try: import pc_config except ImportError: pass
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.properties.polymodel import _ClassKeyProperty, _ModelPathProperty

_CLASS_KEY_PROPERTY = '_class_key_'
_PATH_KEY_PROPERTY  = '_class_path_'

_class_map = {}

## +=+=+ Metaclass controlling the creation of Providence/Clarity polymodel objects.
class ProvidenceClarityPolyClass(db.PropertiedClass):
    """ Populates properties like __root_class__ and __class_hierarchy__ and enforces logic about direct instantiation. """

    def __init__(cls, name, bases, dct):
            
        if name == 'PolyModel':
            super(ProvidenceClarityPolyClass, cls).__init__(name, bases, dct, map_kind=False)
            return

        elif PolyModel in bases:
            if getattr(cls, '__class_hierarchy__', None):
                raise db.ConfigurationError(('%s cannot derive from PolyModel as '
                '__class_hierarchy__ is already defined.') % cls.__name__)
            cls.__class_hierarchy__ = [cls]
            cls.__root_class__ = cls
            super(ProvidenceClarityPolyClass, cls).__init__(name, bases, dct)
            
        else:
            super(ProvidenceClarityPolyClass, cls).__init__(name, bases, dct, map_kind=False)

            cls.__class_hierarchy__ = [c for c in reversed(cls.mro())
                if issubclass(c, PolyModel) and c != PolyModel]

            if cls.__class_hierarchy__[0] != cls.__root_class__:
                raise db.ConfigurationError(
                    '%s cannot be derived from both root classes %s and %s' %
                    (cls.__name__,
                    cls.__class_hierarchy__[0].__name__,
                    cls.__root_class__.__name__))

        _class_map[cls.class_key()] = cls            
            
## +=+=+ Customized polymorphic database model based on Google's PolyModel implementation.
class PolyModel(Model):
    """
    
    Description: A modification to Model designed to introduce polymorphism,
    allowing models to inherit properties and methods from other models.
    Cannot be instantiated directly - designed only to be extended.
    
    Abstract: Once a model is created that extends PolyModel, other models
    can be created that extend the original. In Providence/Clarity, all
    polymorphic types eventually extend the 'E' model (for "Entity").
    
    Example:
    
        -----
        | E |
        -----
          |
          --------------------
             |               |
        -----------       --------
        | GeoArea |       | Role |
        -----------       --------
             |                |
             |                ---------------------
        ------------              |               |
        | US State |         |------------|  |-----------|
        ------------         | Legislator |  | President |
                             |------------|  |-----------|
                                   |
                            ---------------
                            |             |
                        -----------  ---------------     
                        | Senator |  | Congressman |
                        -----------  ---------------

    When a PolyModel object is constructed, there are two special properties
    that are automatically set: _class_key_ (list) and _class_path_ (str).
    The class key describes the object's ancestry, and the class path stores
    the python module path to the corresponding class. For example, let's
    create an object of kind "Senator":
    
        s = Senator(prop1='string',prop2=123)
        s.put()
        
        ## values of special props
        
        print s._class_key_
        >> ('E','Role','Legislator','Senator')
        
        print s._class_path_
        >> ('data','entities','people','Senator')
        
    Since we store the class path along with the class key, PolyModel can
    lazy-load the implementation class when an entity is pulled from the
    datastore:
    
        q = E.all()
        r = q.fetch(50)
        
    ... will automatically import each implementation class as it returns
    fetched results.

    """

    __metaclass__ = ProvidenceClarityPolyClass

    ## stores class inheritance/ancestry (list property)
    _class_property = _ClassKeyProperty(name=_CLASS_KEY_PROPERTY)
    
    ## stores python package import path
    _model_path_property = _ModelPathProperty(name=_PATH_KEY_PROPERTY,indexed=False)
    
    def __new__(cls, *args, **kwds):
        """ Prevents direct instantiation of PolyModel. """
        if cls is PolyModel:
            raise NotImplementedError() # raise NotImplemented
        return super(PolyModel, cls).__new__(cls, *args, **kwds)

    @classmethod
    def kind(cls):
        """ Always return name of root class. """        
        if cls.__name__ == 'PolyModel': return cls.__name__
        else: return cls.class_key()[0]
        

    @classmethod
    def class_key(cls):
        """ Returns class path (in tuple form). """
        if not hasattr(cls, '__class_hierarchy__'):
            raise NotImplementedError('Cannot determine class key without class hierarchy')
        return tuple(cls.class_name() for cls in cls.__class_hierarchy__)

    @classmethod
    def class_name(cls):
        """ Returns the name of the current class. """
        return cls.__name__
    
    @classmethod
    def path_key(cls):
        """ Returns the Python import path for the implementation class (in tuple form). """
        if not hasattr(cls, _PATH_KEY_PROPERTY):
            return tuple(i for i in str(cls.__module__+'.'+cls.__name__).split('.'))
        else:
            path_t = getattr(cls, _PATH_KEY_PROPERTY).split('::')
            return tuple('.'.join(path_t).split('.'))
    
    def path_module(self):
        """ Returns the module part of the Python import path for the implementation class (in tuple form). """
        if not hasattr(self, _PATH_KEY_PROPERTY):
            return tuple(self.__module__.split('.'))
        else:
            path_t = getattr(self, _PATH_KEY_PROPERTY).split('::')
            return tuple(path_t[0].split('.'))

    def path_module_name(self):
        """ Returns the module part of the Python import path for the implementation class (in string form). """
        if not hasattr(self, _PATH_KEY_PROPERTY):
            return str(self.__module__)
        else:
            path_t = getattr(self, _PATH_KEY_PROPERTY).split('::')
            return path_t[0]
            
    @classmethod
    def path_class(cls):
        """ Returns a Python 'class' object of the implementation class. """
        if _class_map[cls.class_key()] is not None:
            return _class_map[cls.class_key()]
        else: return cls
    
    @classmethod
    def from_entity(cls, entity):
    
        if(_PATH_KEY_PROPERTY in entity and
           entity[_PATH_KEY_PROPERTY] != cls.path_key()):
            key = entity[_PATH_KEY_PROPERTY]
            try:
                
                ### split away path from class name
                class_path_t = key.split('::')
                
                #### build and execute an import statement to lazy-load the implementation class
                exec 'from '+class_path_t[0]+' import '+class_path_t[1]

                #### instantiate an empty class of the requested type
                obj = eval(class_path_t[1],globals(),locals())()
                    
                
                #### add the class to the _class_map... polymodel will do the rest
                _class_map[obj.class_key()] = obj.__class__
                
            except ImportError:
                raise db.KindError('Could not import model hierarchy \'%s\'' % str(key))
                
            except NameError:
                raise db.KindError('Could not instantiate model implementation of type "'+str(class_path_t[1])+'", even though import succeeded.')
    
        if (_CLASS_KEY_PROPERTY in entity and
            tuple(entity[_CLASS_KEY_PROPERTY]) != cls.class_key()):
            key = tuple(entity[_CLASS_KEY_PROPERTY])
            try:
                ### this should not fail, as long as the import statement above succeeds
                poly_class = _class_map[key]
            except KeyError:
                raise db.KindError('No implementation for class \'%s\'' % key)
            return poly_class.from_entity(entity)
        return super(PolyModel, cls).from_entity(entity)

    @classmethod
    def all(cls, **kwds):
        query = super(PolyModel, cls).all(**kwds)
        if cls != PolyModel:
            query.filter(_CLASS_KEY_PROPERTY + ' =', cls.class_name())
        return query

    @classmethod
    def gql(cls, query_string, *args, **kwds):
        if cls == cls.__root_class__:
            return super(PolyModel, cls).gql(query_string, *args, **kwds)
        else:
            from google.appengine.ext import gql
            
            query = db.GqlQuery('SELECT * FROM %s %s' % (cls.kind(), query_string))

            query_filter = [('nop',[gql.Literal(cls.class_name())])]
            query._proto_query.filters()[(_CLASS_KEY_PROPERTY, '=')] = query_filter
            query.bind(*args, **kwds)
            return query