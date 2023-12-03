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
##8003



app = FastAPI()

class Demande(BaseModel):
    email: str
    montant: float
    revenu: float
    depenses: float

@app.get("/ServiceSolvabilite/")
async def solvabiliteClient(data: Demande):
        email = data.email
        montant = data.montant
        revenu = data.revenu
        depenses = data.depenses
        
        print(email)
        list_client = []
        result_tuple = {}
        try:
            with open("banque.json", "r") as f:
                list_client = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

        
        dettes = 0  

        for client in list_client:
            print(client["Email"])
            if client["Email"] == email:
                # Récupérer le tuple (nom, prénom, email) correspondant
                result_tuple = client
                dettes = sum(result_tuple["Dete"])
                break

        # Si le client n'est pas trouvé, retourner -1, sinon effectuer le calcul et retourner le résultat
        if dettes == 0:
            response = {"score": -1}
            print(response)
            return response
        else:
            ratio_dettes_montant_pret = dettes / montant if montant != 0 else 0
            ratio_depenses_revenu = depenses / revenu if revenu != 0 else 0
            score = (revenu - depenses)*12 / montant
            if ratio_dettes_montant_pret > 0.3 or ratio_depenses_revenu > 0.5:
            # Pénalité si le ratio dettes/montant_pret ou dépenses/revenu dépasse des seuils critiques
                score *= 0.7
        print(score)
        response = {"score": score}
        print(response)
        return response
