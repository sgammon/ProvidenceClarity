import os
import logging

config = {

    'platform':
    {
        'name':'Providence/Clarity',
        'public':False,
    },
    
    'multitenancy':
    {
        'enable':True,
        'default_namespace':'_global_',
        'force_namespace':False,
        'logging': False,
        'apps_mode_force':False,
        'apps_subdomain':'apps',
    },

    'logging':
    {
        'handler':logging,
        'global_queue':False,
        'tag':True,
        'threshold':'debug'
    },
    
    'api.util':
    {
        'import_logging':False,
    },
    
    'api.storage':
    {
        'adapters':{'datastore':'ProvidenceClarity.api.storage.datastore.DatastoreAdapter',
                    'blobstore':'ProvidenceClarity.api.storage.blobstore.BlobstoreAdapter',
                    'webstorage':'ProvidenceClarity.api.storage.webstorage.WebStorageAdapter'}
    },

    'api.data.proto.ProtoController':
    {
        'log_imports':False,
    },
    
    'data.entity.E':
    {
        'index_on_create':True,
        'cache_on_create':False
    },
    
    'data.core.polymodel.PolyModel':
    {
        'log_imports':True,
        'key_name_seperator':'//',
    },
    
    'decorators.data.QueuedTransaction':
    {
        'default_retries':3,
    },
    
    'handlers':
    {
        'page_caching':False,
        'template_root':'templates/',
        'images_url':'/assets/images/static/p-c/',
        'style_url':'/assets/style/static/p-c/',
        'script_utl':'/assets/script/static/p-c/'
    },
    
    'security':
    {
        'enable_security':False,
    },

}

def get(key,module,default=None):
    
    if module in config:
        if key in config[module]:
            return config[module][key]
        else: return default
    else: return default
    
def dump():
    
    return config    