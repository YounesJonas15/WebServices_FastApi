import json
import sys
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from suds.client import Client


class ServicePropriete(ServiceBase):
    @rpc(Unicode, Unicode, float, Unicode, _returns=float)
    def proprieteClient(ctx, nb_piece, ville, montant, type):
        try:
            with open("ventes_recentes.json", "r") as f:
                data = json.load(f)
                if data:
                    for vente in data:
                        if vente["Ville"] == ville and vente["nombre_piece"]== int(nb_piece) and vente["type"] == type :
                            prix = float(vente.get("prix"))
                            score = montant / prix   # Score basé sur le prix par rapport au prix moyen
                            score = 1 / score
                            return min(1,score)
                    return 0.5  # Aucune vente récente trouvée correspondant aux critères
                else:
                    return 0.5  # Aucune vente récente dans la base de données
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Erreur lors de la lecture du fichier : {str(e)}")
            return -1  # Erreur lors de la lecture du fichier

    
application = Application([ServicePropriete],
                          tns='spyne.examples.propriete',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )
if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'ServicePropriete'),
    ]
    sys.exit(run_twisted(twisted_apps, 8004))