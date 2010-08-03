import os, logging
from ProvidenceClarity import VERSION, PC_PATH, pc_config
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache, users

COMPILED_TEMPLATE_PATH = None

class RequestHandler(webapp.RequestHandler):

    def render_raw(self, content):
        
        self.response.out.write(content)
        
    def render(self, tmpl, vars={}, **kwds):
        
        ######## //    Page   // ########
        ######## //  Caching  // ########
        
        global COMPILED_TEMPLATE_PATH
        
        if pc_config.get('page_caching','handlers',False) == True:
            if 'caching' not in kwds or kwds['caching'] == True:
                user = users.get_current_user()
                if user != None:
                    key = str(tmpl)+'::'+str(user.user_id())
                else:
                    key = str(tmpl)+'::NOT_LOGGED_IN'
                    
                cached_page = memcache.get(key)
                if cached_page != None:
                    
                    # append cached page header if debug headers are turned on
                    if pc_config.get('debug_headers','handlers',False) == True:
                        self.response.headers['X-PC-Is-Cached'] = "true"
                    
                    self.response.out.write(cached_page)
                    return True # finish out if we write a cached page
        
        ######## //   Prepare   // ########
        ######## //  Variables  // ########
        
        ## init vars
        variables = {}
        
        ## prepare page variables
        sys = {'urls':{},'config':{},'security':{},'env':{},'version':VERSION,'subnav':False}
        sys['urls']['images'] = pc_config.get('images_url','handlers','/assets/images/static/')
        sys['urls']['script'] = pc_config.get('script_url','handlers','/assets/script/static/')
        sys['urls']['style'] = pc_config.get('style_url','handlers','/assets/style/static/')
        
        ## platform config
        sys['config'] = pc_config.dump()
        
        ## user & security variables
        if pc_config.get('enable_security','security',True) == True:
            sys['security']['user'] = users.get_current_user()
            sys['security']['permissions'] = {'sys_admin':users.is_current_user_admin()}
            sys['security']['logout_url'] = users.create_logout_url(pc_config.get('logout_destination','security','/'))
            sys['security']['login_url'] = users.create_login_url('/_pc/manage/')
        else:
            sys['security']['user'] = False
            sys['security']['permissions'] = {'sys_admin':False}
            sys['security']['logout_url'] = users.create_logout_url(pc_config.get('logout_destination','security','/'))            
            sys['security']['login_url'] = users.create_login_url('/_pc/manage/')            
        
        ## page variables
        if 'page' in kwds:
            variables['page'] = kwds['page']
        
        ## environment variables
        for name in os.environ.keys():
            sys['env'][name] = os.environ[name]
        
        ## add in sys
        variables['sys'] = sys        
        
        ## add extra vars
        if len(vars) > 0:
            for var in vars.keys():

                # pull subnav
                if key == 'subnav':
                    sys['subnav'] = kwds['subnav']
                else:
                    variables[key] = kwds[key]
    
        ######## //   Render   // ########
        ######## //    Page   // ########
        
        ## get template root
        if COMPILED_TEMPLATE_PATH == None:
            source = PC_PATH
            if PC_PATH[-1] != '/':
                source = source+'/'

            template_root = pc_config.get('template_root','handlers',None)

            if template_root != None and isinstance(template_root, str):
            
                if source[-1] != '/' and template_root[0] != '/':
                    template_root = template_root+'/'
                
                source = source+template_root
            
            if source[-1] != '/' and tmpl[0] != '/':
                source = source+'/'
            
            COMPILED_TEMPLATE_PATH = source
            source = source+tmpl
            
        else:
            source = COMPILED_TEMPLATE_PATH+tmpl
        
        logging.info('SOURCE: '+str(source))
        
        ## set headers, render, and go
        self.render_raw(template.render(source,variables))