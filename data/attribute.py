from google.appengine.ext import db
from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.proto import ProtoModel
from ProvidenceClarity.data.core.polymodel import PolyModel

class A(PolyModel, ProtoModel, CreatedModifiedMixin):
    name = db.StringProperty(indexed=True)