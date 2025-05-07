from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

FILE = "data.json"

class Config(BaseModel):
    horarios: List[int]
    ligar_agora: bool

def carregadar_dados():
    if not os.path.exists(FILE):
        salvar_dados({"horarios": [], "ligar_agora": False})

    with open(FILE, "r") as f:
        return json.load(f)
    
def salvar_dados(dados):
    with open(FILE, "w") as f:
        json.dump(dados, f)

@app.get("/config", response_model=Config)