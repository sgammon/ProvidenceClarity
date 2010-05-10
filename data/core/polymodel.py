from google.appengine.ext import db
from data.core.model import Model
from data.core.polyclass import ProvidenceClarityPolyClass
from data.core.properties import _ClassKeyProperty, _ModelPathProperty

## +=+=+ Customized polymorphic database model based on Google's PolyModel implementation.
class PolyModel(Model):

    __metaclass__ = ProvidenceClarityPolyClass

    _class = _ClassKeyProperty(name=_CLASS_KEY_PROPERTY)
    _model_path = _ModelPathProperty(name=_PATH_KEY_PROPERTY,indexed=False)
    
    def __new__(cls, *args, **kwds):
        """Prevents direct instantiation of PolyModel."""
        if cls is PolyModel:
            raise NotImplementedError()
        return super(PolyModel, cls).__new__(cls, *args, **kwds)

    @classmethod
    def kind(cls):
        #if cls is cls.__root_class__:
            #return super(PolyModel, cls).kind()
        #else:
            #return cls.__root_class__.kind()
        return cls._class

    @classmethod
    def class_key(cls):
        
        if not hasattr(cls, '__class_hierarchy__'):
            raise NotImplementedError('Cannot determine class key without class hierarchy')
        return tuple(cls.class_name() for cls in cls.__class_hierarchy__)

    @classmethod
    def class_name(cls):
        return cls.__name__
    
    @classmethod
    def path_key(cls):
        
        if not hasattr(cls, '__model_hierarchy__'):
            #raise NotImplementedError('Cannot determine model hierarchy without model key')
            return [i for i in str(cls.__module__+'.'+cls.__class__.__name__).split('.')]
        return tuple(i for i in cls.__model_hierarchy__)
    
    @classmethod
    def from_entity(cls, entity):
    
        if(_PATH_KEY_PROPERTY in entity and
           tuple(entity[_PATH_KEY_PROPERTY]) != cls.path_key()):
            key = tuple(entity[_PATH_KEY_PROPERTY])
            try:
                abspath = os.path.abspath(os.path.dirname(__file__))
                if abspath not in sys.path:
                    sys.path.insert(0,abspath)
                    print 'IMPORTING: from '+str('.'.join(key[0:-1]))+' import '+str(key[-1])+"\n"
                    exec 'from '+'.'.join(key[0:-1])+' import '+key[-1]
                    
                    #print 'IMPORT: '+'from '+'.'.join(key[0:-1])+' import '+key[-1]+"\n"
                    obj = eval(key[-1],globals(),locals())()
                    _class_map[obj.class_key()] = obj.__class__
                    print 'OBJ RESULT: '+str(obj)+"\n"
                    print 'CLASS_MAP: '+str(_class_map)+"\n\n"
            except ImportError:
                raise db.KindError('Could not import model hierarchy \'%s\'' % str(key))
    
        if (_CLASS_KEY_PROPERTY in entity and
            tuple(entity[_CLASS_KEY_PROPERTY]) != cls.class_key()):
            key = tuple(entity[_CLASS_KEY_PROPERTY])
            #print 'KEY: '+str(key)+"\n\n"
            try:
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
            query._proto_query.filters()[('class', '=')] = query_filter
            query.bind(*args, **kwds)
            return query