import json
import sys
from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/extractionData/")
async def Extract_donnee_client(data: dict):
    file_path = data.get("file_path")
    print(file_path)
    """
    try:
            # Lire les données depuis le fichier JSON
            with open(file_path, "r") as f:
                demande = json.load(f)

            # Vérifier s'il y a des demandes dans le fichier
            if demande:

                
                data_client = {
                  "Nom du Client": demande["nom"],
                  "Prenom du Client": demande["prenom"],
                  "Ville" : demande["ville"],
                  "Email" : demande["email"],
                  "Type": demande["type_immobilier"],
                  "Montant": float(demande["montant"]),
                  "Nombre de pieces": demande["nombre de pieces"],
                  "Revenu": demande["revenu"],
                  "Depenses": demande["depenses"]
                }
                print(data_client)
                
                response = requests.post("http://127.0.0.1:8002/extractionData/", json = data_client)
                if response.status_code == 200:
                    print(f"File successfully sent.")
                else:
                    print(f"Failed to send file. Status code: {response.status_code}")
                
            else:
                return "Aucune demande de nom trouvée ."
    except (json.JSONDecodeError, FileNotFoundError) as e:
            return f"Erreur lors de la lecture du fichier : {str(e)}"
    """
    return {"message": "File path received successfully"}
