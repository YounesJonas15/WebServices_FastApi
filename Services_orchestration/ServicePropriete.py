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
##8004



app = FastAPI()

class Demande(BaseModel):
    nombre_piece: int
    ville: str
    montant: float
    type: str


@app.get("/ServicePropriete/")
async def proprieteClient(data: Demande):
        nombre_piece = data.nombre_piece
        ville = data.ville
        montant = data.montant
        type = data.type
        try:
            with open("ventes_recentes.json", "r") as f:
                data = json.load(f)
                if data:
                    for vente in data:
                        if vente["Ville"] == ville and vente["nombre_piece"]== int(nombre_piece) and vente["type"] == type :
                            prix = float(vente.get("prix"))
                            score = montant / prix   # Score basé sur le prix par rapport au prix moyen
                            score = 1 / score
                            response = {"score": min(1,score)}
                            return response
                    return {"score": 0.5}  # Aucune vente récente trouvée correspondant aux critères
                else:
                    return {"score": 0.5}  # Aucune vente récente dans la base de données
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Erreur lors de la lecture du fichier : {str(e)}")
            return {"score": -1}  # Erreur lors de la lecture du fichier