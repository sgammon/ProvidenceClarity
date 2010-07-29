from google.appengine.ext import db


class ModelMixin(object):
    __metaclass__ = db.PropertiedClass

    @classmethod
    def kind(self):
        """Need to implement this because it is called by PropertiedClass
        to register the kind name in _kind_map. We just return a dummy name.
        """
        return '__model_mixin__'