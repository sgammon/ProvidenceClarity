from google.appengine.ext import db
from ProvidenceClarity.core import ProvidenceClarityObject
from . import _PC_MODEL_BRANCH_BASE



class Model(db.Model, ProvidenceClarityObject):

    """ Root, master, non-polymorphic data model. Everything lives under this class. """

    _PC_MODEL_BRANCH = _PC_MODEL_BRANCH_BASE
    
    def _setCachedPath(self):
        setattr(self, '_PC_CACHED_PATH', self._getModelPath('.'))
    
    @classmethod
    def _pc_model_branch(cls):
        return cls._PC_MODEL_BRANCH
        

    def _getModelPath(self,seperator=None):

        path = [i for i in str(self.__module__+'.'+self.__class__.__name__).split('.')]

        if seperator is not None:
            return seperator.join(path)

        return path
        

    def _getClassPath(self, seperator=None):

        if hasattr(self, '__class_hierarchy__'):
            path = [cls.__name__ for cls in self.__class_hierarchy__]
        
            if seperator is not None:
                return seperator.join(path)
            return path
        else:
            return False