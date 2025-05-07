from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ARQUIVO = "database.json"

class Config(BaseModel):
    horarios: List[int]
    ligar_agora: bool

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        salvar_dados({"horarios": [], "ligar_agora": False})
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    dados = carregar_dados()
    horarios = ",".join(map(str, dados.get("horarios", [])))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "horarios": horarios,
        "ligar_agora": dados.get("ligar_agora", False)
    })

@app.post("/salvar")
def salvar_horarios(horarios: str = Form(...)):
    lista = [int(h.strip()) for h in horarios.split(",") if h.strip().isdigit()]
    dados = carregar_dados()
    dados["horarios"] = sorted(set(lista))  # remove duplicatas e ordena
    dados["ligar_agora"] = False
    salvar_dados(dados)
    return RedirectResponse("/", status_code=303)

@app.post("/acionar")
def acionar_agora():
    dados = carregar_dados()
    dados["ligar_agora"] = True
    salvar_dados(dados)
    return RedirectResponse("/", status_code=303)

@app.get("/horarios", response_model=Config)
def get_config():
    dados = carregar_dados()
    if dados["ligar_agora"]:
        dados["ligar_agora"] = False  # Resetar automaticamente após leitura
        salvar_dados(dados)
        return {"horarios": dados["horarios"], "ligar_agora": True}
    return dados

@app.post("/horarios")
def set_horarios(config: Config):
    salvar_dados(config.dict())
    return {"mensagem": "Configuração atualizada com sucesso."}
