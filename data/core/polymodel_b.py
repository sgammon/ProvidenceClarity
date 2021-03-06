import logging
import sys
import os

from google.appengine.ext import db
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.properties.polymodel import _ClassKeyProperty
from ProvidenceClarity.data.core.properties.polymodel import _ModelPathProperty

from ProvidenceClarity import pc_config
from ProvidenceClarity.api.data import DataController

_PATH_PREFIX = pc_config.get('path_prefix','api.data.core.polymodel.PolyModel',False)
_IMPORT_PREFIX = pc_config.get('import_prefix','api.data.core.polymodel.PolyModel',False)
_PATH_SEPERATOR = pc_config.get('poly_path_seperator','api.data.core.polymodel.PolyModel',':')
_LOG_IMPORTS = pc_config.get('log_imports','api.data.core.polymodel.PolyModel',False)
_KEY_NAME_SEPERATOR = pc_config.get('key_name_seperator','api.data.core.polymodel.PolyModel','//')

_CLASS_KEY_PROPERTY = pc_config.get('poly_class_field','data','_class_key_')
_PATH_KEY_PROPERTY  = pc_config.get('poly_path_field','data','_class_path_')


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
          ---------------------------------
             |               |            |
        -----------       --------       ----------
        | GeoArea |       | Role |       | Person |
        -----------       --------       ----------
             |                |
             |                |
        ------------          ---------------------
        | US State |              |               |
        ------------        --------------  -------------
                            | Legislator |  | President |
                            --------------  -------------
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
        >> ['E','Role','Legislator','Senator']
        
        print s._class_path_
        >> ['data','entities','people','Senator']
        
    Since we store the class path along with the class key, PolyModel can
    lazy-load the implementation class when an entity is pulled from the
    datastore:
    
        q = E.all()
        r = q.fetch(50)
        
    ... will automatically import each implementation class as it returns
    fetched results.

    """

    __metaclass__ = ProvidenceClarityPolyClass

    ## Stores object ancestry path
    _class_property = _ClassKeyProperty(name=_CLASS_KEY_PROPERTY)
    
    ## Stores Python package import path
    _model_path_property = _ModelPathProperty(name=_PATH_KEY_PROPERTY,indexed=False)
    
    
    def __new__(cls, *args, **kwds):

        """ Prevents direct instantiation of PolyModel. """

        if cls is PolyModel:
            raise NotImplementedError() # raise NotImplemented
        return super(PolyModel, cls).__new__(cls, *args, **kwds)
        
        
    def __init__(self, *args, **kwargs):

        """ Namespaces a given key_name with the kind name prefixed. """

        if 'key_name' in kwargs:

            if len(self.class_key_as_list()) > 1:

                logging.info('namespacing key name')

                kn_split_t = kwargs['key_name'].split(_KEY_NAME_SEPERATOR)
                if kn_split_t[0] == self.class_key()[-1]:
                    self._kn_derived = kwargs['key_name']
                else:
                    self._kn_derived = self.class_key()[-1]+_KEY_NAME_SEPERATOR+kwargs['key_name']
                    kwargs['key_name'] = self._kn_derived

            else:

                logging.info('not namespacing key name')            

        super(PolyModel, self).__init__(*args, **kwargs)
        

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
    def class_key_as_list(cls):

        """ Returns class path (in list form). """

        if not hasattr(cls, '__class_hierarchy__'):
            raise NotImplementedError('Cannot determine class key without class hierarchy')
        return list(cls.class_name() for cls in cls.__class_hierarchy__)


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
            path_t = getattr(cls, _PATH_KEY_PROPERTY).split(_PATH_SEPERATOR)
            return tuple('.'.join(path_t).split('.'))
    

    def path_module(self):

        """ Returns the module part of the Python import path for the implementation class (in tuple form). """

        if not hasattr(self, _PATH_KEY_PROPERTY):
            return tuple(self.__module__.split('.'))
        else:
            path_t = getattr(self, _PATH_KEY_PROPERTY).split(_PATH_SEPERATOR)
            return tuple(path_t[0].split('.'))


    def path_module_name(self):

        """ Returns the module part of the Python import path for the implementation class (in string form). """

        if not hasattr(self, _PATH_KEY_PROPERTY):
            return str(self.__module__)
        else:
            path_t = getattr(self, _PATH_KEY_PROPERTY).split(_PATH_SEPERATOR)
            return path_t[0]
            

    @classmethod
    def path_class(cls):

        """ Returns a Python 'class' object of the implementation class. """

        if _class_map[cls.class_key()] is not None:
            return _class_map[cls.class_key()]
        else: return cls
    

    @classmethod
    def from_entity(cls, entity):
    
        #logging.info(' ')
        #logging.info('========== PRE CLASS MAP DUMP ==========')
        
        #if len(_class_map) > 0:
                        
        #    for key in _class_map.keys():

        #        if key is None:
        #            logging.info('-- :: NONE KEY ::  =>  '+str(_class_map[key]))
        #        else:
        #            logging.info('--'+str(key)+'  =>  '+str(_class_map[key]))
             
        #logging.info('======== END PRE CLASS MAP DUMP ========')
        #logging.info(' ')
        
        logging.info(' ')        
        logging.info('============= PolyModel Entity Unpack ============= ')
        logging.info('class_key: '+str(cls.class_key()))
        logging.info('path_key: '+str(cls.path_key()))
        logging.info('cls: '+str(cls))
    
        if _CLASS_KEY_PROPERTY in entity:
            
            #if tuple(entity[_CLASS_KEY_PROPERTY]) != cls.class_key():
            #    logging.info('Model is not of base poly type E.')

            key = tuple(entity[_CLASS_KEY_PROPERTY])

            #if key in _class_map:

            #    logging.info('Key found in classmap. ('+str(_class_map[key])+')')
                
            #    poly_class = _class_map[key]
                
            #    rez = poly_class().from_entity(entity)
            #    logging.info('Resulting Entity: '+str(rez))
                
            #    return rez

        
            #else:
            #    logging.info('Key NOT found in classmap.')
                
            if(_PATH_KEY_PROPERTY in entity and entity[_PATH_KEY_PROPERTY] != cls.path_key()):

                logging.info('Model path is not equal to default.')

                key = entity[_PATH_KEY_PROPERTY]
                
                try:

                    logging.info('Attempting lazy-load.')
            
                    ### split away path from class name
                    class_path_t = key.split(_PATH_SEPERATOR)
        
                    #### build and execute an import statement to lazy-load the implementation class
                    if _IMPORT_PREFIX is not False:
                        if _IMPORT_PATH[-1] != '.': _IMPORT_PATH = _IMPORT_PATH+'.'
                        prefix = _IMPORT_PATH
                    else:
                        prefix = ''
                        
                    logging.info('Executing import request: '+str(class_path_t)+'.')

                    if _LOG_IMPORTS == True: logging.debug('[PolyModel]: Importing data class "'+str(class_path_t[-1])+'" from "'+str(prefix.join(class_path_t[0:-1]))+'".')
                    imported_class = DataController.import_model(class_path_t)

                    #### instantiate an empty class of the requested type
                    logging.info('Imported Class: '+str(imported_class))
                    logging.info('Attribute Request: '+str(class_path_t[-1]))
                    
            
                    #obj = getattr(imported_class,class_path_t[-1])()
                    obj = imported_class()

                    logging.info('Creating object... '+str(obj))
                    logging.info('Adding to Classmap: "'+str(obj.__class__)+'" with key "'+str(obj.class_key())+'".')
        
                    #### add the class to the _class_map... polymodel will do the rest
                    _class_map[obj.class_key()] = obj.__class__

                    ## Return Entity
                    logging.info('Lazy load successful. Creating entity...')
                                    
                    found_entity = obj.from_entity(entity)
        
                    logging.info('Resulting Entity: '+str(found_entity))
                    
                    return found_entity
                        
#                        else:
#                            logging.critical('Could not find attribute "'+str(class_path_t[-1])+'" on class "'+str(imported_class)+'".')
#                            logging.critical('PolyModel expansion resulted in failure. Terminating.')
#                            logging.info(' ')
            
                except ImportError:
                    logging.error('[PolyModel]: Error importing data class "'+str(class_path_t)+'".')
                    raise db.KindError('Could not import model hierarchy \'%s\'' % str(key))
        
                except NameError:
                    logging.error('[PolyModel]: Error instantiating data class "'+str(class_path_t)+'".')
                    raise db.KindError('Could not instantiate model implementation of type \'%s\'' % str(class_path_t[-1]))
        
        #else:
        #    logging.critical('Model IS of base poly type E.')
        #    logging.critical('PolyModel expansion resulted in failure. Terminating.')
        #    logging.info(' ')



    @classmethod
    def get_by_key_name(cls, key_names, parent=None):
        
        if len(cls.class_key_as_list()) == 1:
            kn_derived = key_names
            
        else:
            if isinstance(key_names, str):
                kn_split_i = key_names.split(_KEY_NAME_SEPERATOR)

                if kn_split_i[0] == cls.class_key()[-1]:
                    kn_derived = key_names
                
                else: kn_derived = cls.class_key()[-1]+_KEY_NAME_SEPERATOR+key_names

            elif isinstance(key_names, list):

                kn_derived = []
                for item in key_names:
                    kn_split_t = item.split(_KEY_NAME_SEPERATOR)
                    if kn_split_i[0] == cls.class_key()[-1]:
                        kn_derived.append(item)
                
                    else: kn_derived.append(cls.class_key()[-1]+_KEY_NAME_SEPERATOR+item)
                
        return super(PolyModel, cls).get_by_key_name(kn_derived, parent)


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