import json
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import requests
"""from suds.client import Client"""
from email.message import EmailMessage
##8005


class Demande(BaseModel):
    solvabilite_score: float
    propriete_score: float
app = FastAPI()

@app.get("/ServiceDecision/")
async def decisionClient(data: Demande):
        solvabilite = data.solvabilite_score
        priorite = data.propriete_score
        if (solvabilite + priorite)/2 >= 0.5:
            return {"decision" : True}
        else : 
            return {"decision" : False}
           
