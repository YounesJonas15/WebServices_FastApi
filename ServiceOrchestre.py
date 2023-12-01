import json
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from suds.client import Client
from email.message import EmailMessage
import smtplib 
import ssl



app = FastAPI()

@app.post("/Orchestration/")
async def orchestration(data: dict):
    file_path = data.get("file_path")
    print(file_path)
    """
    response = requests.post("http://127.0.0.1:8002/extractionData/", json={"file_path": file_path})

    if response.status_code == 200:
        print("File path successfully sent to extraction service.")
    else:
        print(f"Failed to send file path to extraction service. Status code: {response.status_code}")
    """
    return {"message": "File path received successfully"}


    
