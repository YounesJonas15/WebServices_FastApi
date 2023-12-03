import json
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import requests
"""from suds.client import Client"""
from email.message import EmailMessage
import smtplib 
import ssl




app = FastAPI()

class Demande(BaseModel):
    file_path: str

@app.post("/Orchestration/")
async def orchestration(data: Demande):
    file_path = data.file_path
    print(file_path)
    
    #Extraction des information
    response = requests.get("http://127.0.0.1:8002/extractionData/", json={"file_path": file_path})
    
    if response.status_code == 200:
        print("File path successfully sent to extraction service.")
        demande = response.json()
        print(demande)
    else:
        print(f"Failed to send file path to extraction service. Status code: {response.status_code}")
    

    # Service de solvabilite
    data = {
        "email" : demande["Email"],
        "montant" : demande["Montant"],
        "revenu" : demande["Revenu"],
        "depenses" : demande["Depenses"]
    }
    response = requests.get("http://127.0.0.1:8003/ServiceSolvabilite/", json=data)
    solvabilite_score = float(response.json().get("score"))
    
    if solvabilite_score == -1:
        print("Vous n'êtes pas enregistré dans la banque.")
        return("Vous n'êtes pas enregistré dans la banque.")
    else:
        print(solvabilite_score)
    
    # Service de propriete
    data = {
        "nombre_piece" : demande["Nombre de pieces"],
        "ville" : demande["Ville"],
        "montant" : demande["Montant"],
        "type" : demande["Type"]
    }

    response = requests.get("http://127.0.0.1:8004/ServicePropriete/", json=data)
    propriete_score = float(response.json().get("score"))
    print(propriete_score)

    ##decision final
    data = {
        "solvabilite_score" : solvabilite_score,
        "propriete_score" : propriete_score
    }
    
    response = requests.get("http://127.0.0.1:8005/ServiceDecision/", json=data)
    decision = bool(response.json().get("decision"))

    #enregistrement de la décision
    nom =demande["Nom du Client"]
    prenom = demande["Prenom du Client"]
    email = demande["Email"]
    file_name = f"{nom + prenom}.json"  
    file_path = os.path.join("ResultatDemandes", file_name) 

    resultat_data = {
        "Nom du Client": nom,
        "Prenom du Client": prenom,
        "Email" : email,
        "Reponse": "Pret accorde" if decision else "Pret refuse"
    }

    with open(file_path, "w") as f:
        json.dump(resultat_data, f, indent=4)
    
    #Envoie du mail
    email_sender = 'yassinesoatp@gmail.com'
    email_password = 'ibyk omnw lzuh ytir'

    email_recever = email

    subject = "Décision final pour votre demande"
    if(decision):
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
        
        

        
        
        
    

    return {"message": "File path received successfully"}


    
