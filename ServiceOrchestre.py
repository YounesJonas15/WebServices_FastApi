import json
import os
import sys
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from suds.client import Client
from email.message import EmailMessage
import smtplib 
import ssl

class ServiceOrchestration(ServiceBase):
    @rpc(Unicode,_returns=str)
    def Orchestration(ctx,file_name):
        #Extraction des information

        extractionDonneClientService_client = Client('http://localhost:8002/ServiceExtractionClient?wsdl')
        nom, prenom, ville, email,type, montant, nombre_piece, revenu, depenses = extractionDonneClientService_client.service.Extraction_donne_client(file_name)
        print(nom[1])
        print(prenom[1])

        # Service de solvabilite
        solvabilite_calcul = Client('http://localhost:8003/ServiceSolvabilite?wsdl')
        solvabilite_score = solvabilite_calcul.service.solvabiliteClient( email[1], montant[1], revenu[1], depenses[1])
        if solvabilite_score == -1:
            return("Vous n'êtes pas enregistré dans la banque.")
        else:
            print(solvabilite_score)
        # Service de propriete
        propriete_calcul = Client('http://localhost:8004/ServicePropriete?wsdl')
        propriete_score = propriete_calcul.service.proprieteClient(nombre_piece[1],ville[1],montant[1],type[1])
        print(propriete_score)
        decisionService = Client('http://localhost:8005/ServiceDecision?wsdl')
        finalDecision = decisionService.service.decisionClient(solvabilite_score, propriete_score)
        
        #ebregistrement de la décision
        file_name = f"{nom[1]+prenom[1]}.json"  
        file_path = os.path.join("ResultatDemandes", file_name) 

        resultat_data = {
            "Nom du Client": nom[1],
            "Prenom du Client": prenom[1],
            "Email" : email[1],
            "Reponse": "Pret accorde" if finalDecision else "Pret refuse"
        }

        with open(file_path, "w") as f:
            json.dump(resultat_data, f, indent=4)
        
        #Envoie du mail
        email_sender = 'yassinesoatp@gmail.com'
        email_password = 'ibyk omnw lzuh ytir'

        email_recever = email[1]

        subject = "Décision final pour votre demande"
        if(finalDecision):
            body ="Nous avons le plaisir de vous informer que votre demande de pret immobilier a été accordée "
        else :
            body = "Nous avons le regret de vous informer que votre demande de pret immobilier a été refusé"
            
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_recever
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_recever, em.as_string())
        
        

        
        
        
    
application = Application([ServiceOrchestration],
                          tns='spyne.examples.orchestration',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    twisted_apps = [
        (wsgi_app, b'ServiceOrchestration'),
    ]
    sys.exit(run_twisted(twisted_apps, 8001))
