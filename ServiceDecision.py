import json
import sys
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from suds.client import Client


class ServiceDecision(ServiceBase):
    @rpc( float, float, _returns=bool)
    def decisionClient(ctx, solvabilite, priorite):
        if (solvabilite + priorite)/2 >= 0.5:
            return True
        else : 
            return False
           
    
application = Application([ServiceDecision],
                          tns='spyne.examples.decision',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )
if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'ServiceDecision'),
    ]
    sys.exit(run_twisted(twisted_apps, 8005))