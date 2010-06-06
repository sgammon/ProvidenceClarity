from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache, users
from ProvidenceClarity.main import *

class RequestHandler(ProvidenceClarity, webapp.RequestHandler):
    
    def render(self,page,**kwds):
        
        ######## //    Page   // ########
        ######## //  Caching  // ########
        
        if self.config.get('page_caching','handlers',False) == True:
            if 'caching' not in kwds or kwds['caching'] == True:
                user = users.get_current_user()
                if user != None:
                    key = str(page)+'::'+str(user.user_id())
                else:
                    key = str(page)+'::NOT_LOGGED_IN'
                    
                cached_page = memcache.get(key)
                if cached_page != None:
                    
                    # append cached page header if debug headers are turned on
                    if self.config.get('debug_headers','handlers',False) == True:
                        self.response.headers['X-PC-Is-Cached'] = "true"
                    
                    self.response.out.write(cached_page)
                    return True # finish out if we write a cached page
        
        ######## //   Prepare   // ########
        ######## //  Variables  // ########
        
        ## init vars
        variables = {}
        
        ## prepare page variables
        sys = {'urls':{},'config':{},'security':{},'env':{},'config_path':self.config_path,'version':self.version,'subnav':False}
        sys['urls']['images'] = self.config.get('images_url','handlers','/assets/images/static/')
        sys['urls']['script'] = self.config.get('script_url','handlers','/assets/script/static/')
        sys['urls']['style'] = self.config.get('style_url','handlers','/assets/script/style/')
        
        ## platform config
        sys['config'] = self.config.dump()
        
        ## user & security variables
        if self.config.get('enable_security','security',True) == True:
            sys['security']['user'] = users.get_current_user()
            sys['security']['permissions'] = {'sys_admin':users.is_current_user_admin(),'is_human':False}
        else:
            sys['security']['user'] = None
            sys['security']['permissions'] = {'sys_admin':None,'is_human':None}
        
        ## environment variables
        for name in os.environ.keys():
            sys['env'][name] = os.environ[name]
        
        ## add in sys
        variables['system'] = sys        
        
        ## add extra vars
        for key in kwds.keys():

            # pull subnav
            if key == 'subnav':
                sys['subnav'] = kwds['subnav']
            else:
                variables[key] = kwds[key]
    
        ######## //   Render   // ########
        ######## //    Page   // ########
        
        ## get template root
        template_path = self.config.get('template_root','handlers',None)
        
        source = ''
        ## create template path
        if template_path != None:
            source = template_path
        source = source+page
        
        ## set headers, render, and go
        rendered_page = template.render(templ)