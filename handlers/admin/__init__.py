from .. import RequestHandler


class IndexHandler(RequestHandler):
    
    """ Template: admin_base.html """
    
    def get(self):
        
        self.render_raw('<b>Admin IndexHandler</b>')