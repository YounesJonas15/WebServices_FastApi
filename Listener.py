import os
import time
from suds.client import Client

def listener(path):
    dirs = os.listdir(path)
    before = set(dirs)
    while True:
        after = set(os.listdir(path))
        added = after - before
        if added:
            for file_name in added:
                print(file_name)
                
                fichier_ajoute = path + "/" + file_name
                # Appel du service d'orchestration
                orchestre_Reception = Client('http://localhost:8001/ServiceOrchestration?wsdl')
                result = orchestre_Reception.service.Orchestration(fichier_ajoute)
                #print(result)
        before = after

listener("demandes")

