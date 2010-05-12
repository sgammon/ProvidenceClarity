import os

config = {


    'data':
    {
        'index_on_put': True
    }


}


def get(key,module,default=None):
    
    if module in config:
        if key in config[module]:
            return config[module][key]
        else: return default
    else: return default
    
os.environ['PC_CONFIG_LOADED'] = True
os.environ['PC_CONFIG_DEFAULT'] = True