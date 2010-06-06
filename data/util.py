from google.appengine.ext import db


class CreatedModifiedMixin:
    
    ## Created/Modified audit fields
    modified = db.DateTimeProperty(required=True,default=None,auto_now=True)
    created = db.DateTimeProperty(required=True,default=None,auto_now_add=True)
    
    ## Methods for access
    def modified(self):
        return self.modified
        
    def created(self):
        return self.created