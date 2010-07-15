import logging, random, datetime, hashlib

from google.appengine.ext import db
from google.appengine.api import memcache

import exceptions
from ProvidenceClarity import pc_config
from ProvidenceClarity.data.security import SecurityKey, GenericKey, AccountKey

## API for managing SecurityAccounts
class AccountController(object):
    
    @classmethod
    def provision_account(cls, **kwargs):
        pass
        
    @classmethod
    def provision_group_account(cls, **kwargs):
        pass
        
    @classmethod
    def provision_user_account(cls, **kwargs):
        pass
        
    @classmethod
    def provision_machine_account(cls, **kwargs):
        pass
        
    @classmethod
    def retrieve_account(cls, **kwargs):
        pass
    

## API for managing SecurityKeys
class KeyController(object):
    
    
    ### Key Methods
    
    @classmethod
    def provision_key(cls, **kwargs):
        
        key_value, key_hash = cls.provision_key_content()
        
        return (key_value, GenericKey(key_name=key_value, content=key_value, md5_hash=key_hash, **kwargs).put())
        
    @classmethod
    def provision_account_key(cls, account_obj=None, **kwargs):
        
        if account_obj is not None:
        
            key_value, key_hash = cls.provision_key_content(str(account_obj.key()),pc_config.get('account_key_hash_algorithm','security',pc_config.get('key_default_hash_algorithm','security','sha256')))
            
            return (key_value, AccountKey(key_name=key_value, content=key_value, md5_hash=key_hash, account=account_obj, **kwargs).put())
            
        else:
            return False
            
    @classmethod
    def retrieve_key(cls, key_value):
        
        k = SecurityKey.get_by_key_name(key_value)
        k.last_use = datetime.datetime.now()
        
        k.put()
        
        return k
        
    @classmethod
    def use_key(cls, key_value):
        
        k = SecurityKey.get_by_key_name(key_value)
        k.last_use = datetime.datetime.now()
        k.use_tally = k.use_tally+1
        
        k.put()
        
        return k

    @classmethod
    def provision_key_content(cls, salt='', algorithm=pc_config.get('key_default_hash_algorithm','security','sha256')):
        
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(str(salt)+':::'+str(datetime.datetime.now().isoformat())+str(random.random()))
        
        key_hash = hashlib.new('md5')
        key_hash.update(hash_obj.hexdigest())
        
        return (hash_obj.hexdigest(), key_hash.hexdigest())

    @classmethod
    def expire_key(cls, key_value):
        
        key = SecurityKey.get_by_key_name(key_value)
        key.expired = True
        key.put()
        
    @classmethod
    def ban_key(cls, key_value, reason=''):
        
        key = SecurityKey.get_by_key_name(key_value)
        key.banned=True
        key.banned_reason = reason
        
        key.put()
        
    
    ## Token Methods
    
    @classmethod
    def provision_token(cls):
        
        key_value, key_hash = cls.provision_key_content(str(account_obj.key()),pc_config.get('token_key_hash_algorithm','security',pc_config.get('security','key_default_hash_algorithm','md5')))
    
        return (key_value, Token(key_name=key_value, content=key_value, md5_hash=key_hash).put())
        
    @classmethod
    def use_token(cls, token_value):
        
        t = Token.get_by_key_name(token_value)
        if t is not None:
           t.delete()
           return True 
        else:
            raise exceptions.KeyNotFound