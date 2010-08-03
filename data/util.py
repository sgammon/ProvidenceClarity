from google.appengine.ext import db
from ProvidenceClarity.data.core.mixin import ModelMixin


class CreatedModifiedMixin(ModelMixin):
    
    ## Created/Modified audit fields
    dateModified = db.DateTimeProperty(required=True,default=None,auto_now=True,indexed=True,verbose_name="Record Modified")
    dateCreated = db.DateTimeProperty(required=True,default=None,auto_now_add=True,indexed=True,verbose_name="Record Created")
    
    ## Methods for access
    def date_modified(self):
        return self.dateModified
        
    def date_created(self):
        return self.dateCreated


class UserAuditMixin(ModelMixin):
    
    ## User Audit Fields
    userModified = db.UserProperty(auto_current_user=True)    
    userCreated = db.UserProperty(auto_current_user_add=True)
    
    ## Methods for access
    def user_modified(self):
        return self.userModified
        
    def user_created(self):
        return self.userCreated