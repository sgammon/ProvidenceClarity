import os

if 'PC_CONFIG_LOADED' not in os.environ:
    try:
        import pc_config_default
    except ImportError:
        pass