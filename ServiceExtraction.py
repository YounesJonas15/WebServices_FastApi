import json
import sys
from spyne import Application, rpc, ServiceBase, Unicode, Array, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from suds.client import Client

class ServiceExtraction(ServiceBase):
    @rpc(Unicode,_returns=(Unicode, Unicode, Unicode, Unicode, Unicode ,float, Unicode, Unicode, Unicode))
    def Extraction_donne_client(ctx,file_name):
        try:
            # Lire les données depuis le fichier JSON
            with open(file_name, "r") as f:
                data = json.load(f)

            # Vérifier s'il y a des demandes dans le fichier
            if data:

                print(data) 
                return data["Nom du Client"], data["Prenom du Client"], data["Ville"], data["Email"],data["Type"],float(data["Montant"]), data["Nombre de pieces"], data["Revenu"], data["Depenses"]
                

            else:
                return "Aucune demande de nom trouvée ."
        except (json.JSONDecodeError, FileNotFoundError) as e:
            return f"Erreur lors de la lecture du fichier : {str(e)}"
        
         

application = Application([ServiceExtraction],
                          tns='spyne.examples.extraction',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )


if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'ServiceExtractionClient'),
    ]
    sys.exit(run_twisted(twisted_apps, 8002))

















# Ouvrir le fichier JSON
#with open('demande.json', 'r') as json_file:
 #   data = json.load(json_file)
    
#print(data)
