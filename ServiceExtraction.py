import json
import sys
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/extractionData/")
async def Extract_donnee_client(data: dict):
    file_path = data.get("file_path")
    print(file_path)
    print(file_path)
    try:
        # Lire les données depuis le fichier JSON
        with open(file_path, "r") as f:
            demande = json.load(f)
            print("demandes: ")
            print(demande)

        # Vérifier s'il y a des demandes dans le fichier
        if demande:

            print("fichier ouvert avec succès")
            data_client = {
              "Nom du Client": demande["nom"],
              "Prenom du Client": demande["prenom"],
              "Ville" : demande["ville"],
              "Email" : demande["email"],
              "Type": demande["type_immobilier"],
              "Montant": float(demande["montant"]),
              "Nombre de pieces": int(demande["nombre de pieces"]),
              "Revenu": float(demande["revenu"]),
              "Depenses": float(demande["depenses"])
            }
            print(data_client)
            return data_client
                
        else:
            return "Aucune demande de nom trouvée ."
    except (json.JSONDecodeError, FileNotFoundError) as e:
            return f"Erreur lors de la lecture du fichier : {str(e)}"
    
   
