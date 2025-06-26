from fastapi import FastAPI
import requests

app = FastAPI()

API_URL = "https://zerogpt.p.rapidapi.com/api/v1/detectText"
API_KEY = "300b69af1bmsh57cb53a11b27045p1bd0a1jsn9e4528fbcece"
API_HOST = "zerogpt.p.rapidapi.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

@app.get("/")
def analyze_text(text: str):
    payload = {"input_text": text}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        # Verifica se a chave "result" existe
        if "result" not in data:
            return {
                "erro": "Resposta da API não contém 'result'",
                "resposta_completa": data
            }

        score = data["result"].get("is_gpt_generated", "desconhecido")
        return f"Seu texto foi {score} gerado por IA."

    except Exception as e:
        return {"erro": str(e)}



