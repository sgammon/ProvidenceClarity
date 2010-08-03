from .. import RequestHandler


class ReceiverHandler(RequestHandler):

    def get(self, receiver_key=False):
        
        self.render_raw('<b>ReceiverHandler Info: </b>'+str(receiver_key))

    def post(self, receiver_key=False):
        
        self.render_raw('<b>ReceiverHandler</b>')