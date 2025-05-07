from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

horarios = []

class Horario(BaseModel):
    horarios: List[int]

@app.get("/")
def home():
    return {"message": "API para controle de servo motor"}

@app.get("/horarios")
def get_horarios():
    return {"horarios": horarios}

@app.post("/horarios")
def set_horarios(horario: Horario):
    global horarios
    horarios = horario.horarios
    return {"message": "Horários atualizados com sucesso", "horarios": horarios}