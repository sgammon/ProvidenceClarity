# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {
 
    'tipfy': 
    {   
        'middleware':
        [
            'tipfy.ext.debugger.DebuggerMiddleware',
            #'tipfy.ext.appstats.AppstatsMiddleware'
        ],
        
        'apps_installed': ['coi'],
    },
    
    'tipfy.ext.jinja2':
    {
        'templates_dir': 'app/templates',
        'templates_compiled_target': 'app/templates/compiled',
        'force_use_compiled': False
    },
    
    'tipfy.ext.auth':
    {
        'auth_system': 'tipfy.ext.auth.AppEngineAuth',
        'cookie_key': 'coi.auth',
        'domain': '.coi.providenceclarity.com',
        'cookie_secure': True,
        'cookie_http_only': True
    },
    
    'tipfy.ext.i18n':
    {
        'locale': 'en_US',
        'timezone': 'America/Los_Angeles',
        'cookie_name': 'coi.locale',
        'locale_request_lookup': [('args','lc'),('cookies','coi.locale'),('form','locale')]
    },
    
    'tipfy.ext.session':
    {
        'session_type': 'securecookie',
        'secret_key': 'ASDKJI!H)FHF$)8hv8vbh49bgd9b9FH(I!NC*H)',
        'session_cookie_name': 'coi.session',
        'flash_cookie_name': 'coi.message',
        'cookie_domain': '.coi.providenceclarity.com',
        'cookie_secure': True,
        'cookie_http_only': True
    },
}