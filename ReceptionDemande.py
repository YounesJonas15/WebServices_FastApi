import os
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Demande(BaseModel):
    nom: str
    prenom: str
    ville: str
    email: str
    type_immobilier: str
    montant: str
    nombre_piece: str
    revenu: str
    depenses: str


@app.post("/reception_demande/")
async def recevoir_demande(demande: Demande):
    demande_data = {
        "nom": demande.nom,
        "prenom": demande.prenom,
        "ville": demande.ville,
        "email": demande.email,
        "type_immobilier": demande.type_immobilier,
        "montant": demande.montant,
        "nombre de pieces": demande.nombre_piece,
        "revenu": demande.revenu,
        "depenses": demande.depenses
    }

    
    file_name = f"{demande.nom + demande.prenom}.json"
    file_path = os.path.join("demandes", file_name)

    with open(file_path, "w") as f:
        json.dump(demande_data, f, indent=4)
    return {"message": "Demande reçue avec succès"}
