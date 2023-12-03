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
    nom: str
    prenom: str
    ville: str
    email: str
    type_immobilier: str
    montant: float
    nombre_piece: int
    revenu: float
    depenses: float

@app.post("/Orchestration/")
async def orchestration(data: dict):
    file_path = data.get("file_path")
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
    ##response = requests.get("http://127.0.0.1:8005/ServiceDecision/", json=data)
    

    return {"message": "File path received successfully"}


    
