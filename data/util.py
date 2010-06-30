from google.appengine.ext import db


class CreatedModifiedMixin:
    
    ## Created/Modified audit fields
    dateModified = db.DateTimeProperty(required=True,default=None,auto_now=True,indexed=True,verbose_name="Record Modified")
    dateCreated = db.DateTimeProperty(required=True,default=None,auto_now_add=True,indexed=True,verbose_name="Record Created")
    
    ## Methods for access
    def modified(self):
        return self.dateModified
        
    def created(self):
        return self.dateCreated