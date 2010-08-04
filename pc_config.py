import os
import logging

config = {

    'platform':
    {
        'name':'Providence/Clarity',
        'public':False
    },

    'logging':
    {
        'handler':logging,
        'tag':True,
        'threshold':'debug'
    },
    
    'api.data.proto.ProtoController':
    {
        'log_imports':False,
    },
    
    'data':
    {
        'index_on_put': True,
    },
    
    'data.core.polymodel.PolyModel':
    {
        'log_imports':False,
        'path_prefix': False,
        'import_prefix': False,
        'key_name_seperator':'//',
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
    }

}

def get(key,module,default=None):
    
    if module in config:
        if key in config[module]:
            return config[module][key]
        else: return default
    else: return default
    
def dump():
    
    return config    