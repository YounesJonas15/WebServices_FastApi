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
##8005



app = FastAPI()

@app.get("/ServiceDecision/")
async def decisionClient(data: dict):
        solvabilite = data.get("solvabilite_score")
        priorite = data.get("propriete_score")
        if (solvabilite + priorite)/2 >= 0.5:
            return {"decision" : True}
        else : 
            return {"decision" : False}
           
