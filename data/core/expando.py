from . import _PC_MODEL_BRANCH_EXPANDO
from google.appengine.ext import db


class Expando(db.Expando):
    
    _PC_MODEL_BRANCH = _PC_MODEL_BRANCH_EXPANDO