import sys, datetime
from google.appengine.ext import db

from ProvidenceClarity import pc_config as config

from ProvidenceClarity.data.util import CreatedModifiedMixin
from ProvidenceClarity.data.core.model import Model
from ProvidenceClarity.data.core.polymodel import PolyModel

from ProvidenceClarity.api.data import DataManager


class SecurityAccount(PolyModel):

    """ Abstract root class for a security account. """
    
    # Security Flags
    on_watch = db.BooleanProperty(default=False)
    activated = db.BooleanProperty(default=False)
    banned = db.BooleanProperty(default=False)
    banned_reason = db.StringProperty(indexed=False)
    do_captcha = db.BooleanProperty(indexed=True)
    
    # Access Flags
    user_rank = db.IntegerProperty(default=1)
    beta_access = db.BooleanProperty(default=False)
    
    # Timestamps
    last_login = db.DateTimeProperty()
    

class GroupAccount(SecurityAccount):
    
    """ Represents a group of security accounts. """
    
    account_list = db.ListProperty(db.Key)


class UserAccount(SecurityAccount):
    
    """ Security account linked to a user. """
    
    user = db.UserProperty()
    
    pass
    

class MachineAccount(SecurityAccount):
    
    """ Security account used/access by a machine.  """
    
    machine_id = db.StringProperty()
    
    pass
    
    
class SecurityKey(PolyModel, CreatedModifiedMixin):
    
    """ Abstract root class for a security access key. """
    
    ## Key Content
    content = db.StringProperty()
    md5_hash = db.StringProperty()

    ## Key Activation
    activated = db.BooleanProperty(default=False)
    banned = db.BooleanProperty(default=False)
    banned_reason = db.StringProperty(default='')

    ## Automatic Expiration
    expired = db.BooleanProperty(default=False) # Mark as expired
    lifetime = db.IntegerProperty(default=None) # Time-to-live in seconds
    expiration = db.DateTimeProperty(default=None) # Specific date/time for expiration
    
    ## Tallies
    use_tally = db.IntegerProperty(default=0)
    error_tally = db.IntegerProperty(default=0)
    invalid_tally = db.IntegerProperty(default=0)
    
    last_use = db.DateTimeProperty()
        

class GenericKey(SecurityKey):
    
    """ Key designed for access more than once. """
    
    pass


class AccountKey(SecurityKey):
    
    """ Key attached to a SecurityAccount. """
    
    account = db.ReferenceProperty(SecurityAccount, collection_name="keys")
    
    
class Token(SecurityKey):
    
    """ Key designed for one-time-access. """
    
    pass
    

## Proto Inserts

class ProtoHelper(DataManager):

    def insert(self):
        
        self.models.append(self.P(_class=SecurityAccount,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique account ID, given by the App Engine users API for user objects and the unique group name for groups.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=GroupAccount,
                                    direct_parent=db.Key.from_path('Proto','SecurityAccount'),ancestry_path=['SecurityAccount'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique group name generated by Security API.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=UserAccount,
                                    direct_parent=db.Key.from_path('Proto','SecurityAccount'),ancestry_path=['SecurityAccount'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique user object ID.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=MachineAccount,
                                    direct_parent=db.Key.from_path('Proto','SecurityAccount'),ancestry_path=['SecurityAccount'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Unique machine name generated by Security API.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=SecurityKey,
                                    direct_parent=None,ancestry_path=[],abstract=True,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Key value, generated by the Security API.',keyid_use=None,keyparent_use=None))
        
        self.models.append(self.P(_class=GenericKey,
                                    direct_parent=db.Key.from_path('Proto','SecurityKey'),ancestry_path=['SecurityKey'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Key value, generated by the Security API.',keyid_use=None,keyparent_use=None))
                                   
        self.models.append(self.P(_class=AccountKey,
                                    direct_parent=db.Key.from_path('Proto','SecurityKey'),ancestry_path=['SecurityKey'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=True,uses_id=False,
                                   created_modified=True,keyname_use='Key value, generated by the Security API.',keyid_use=None,keyparent_use='Parent account.'))
                                   
        self.models.append(self.P(_class=Token,
                                    direct_parent=db.Key.from_path('Proto','SecurityKey'),ancestry_path=['SecurityKey'],abstract=False,derived=True,is_data=False,poly_model=True,uses_keyname=True,uses_parent=False,uses_id=False,
                                   created_modified=True,keyname_use='Token value, generated by the Security API.',keyid_use=None,keyparent_use=None))
        
        
        return self.models

    def clean(self):
        
        self.models.append(self.P.get_by_key_name('SecurityAccount'))
        self.models.append(self.P.get_by_key_name('GroupAccount'))
        self.models.append(self.P.get_by_key_name('UserAccount'))
        self.models.append(self.P.get_by_key_name('MachineAccount'))
        self.models.append(self.P.get_by_key_name('SecurityKey'))
        self.models.append(self.P.get_by_key_name('GenericKey'))
        self.models.append(self.P.get_by_key_name('AccountKey'))
        self.models.append(self.P.get_by_key_name('Token'))
        
        return self.models