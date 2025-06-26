from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
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

# Página com formulário (GET)
@app.get("/", response_class=HTMLResponse)
async def form():
    return """
        <html>
            <head>
                <title>Analisar Texto com IA</title>
            </head>
            <body>
                <h2>Cole seu texto abaixo:</h2>
                <form method="post">
                    <textarea name="text" rows="20" cols="100"></textarea><br>
                    <button type="submit">Analisar</button>
                </form>
            </body>
        </html>
    """

# Resultado da análise (POST)
@app.post("/", response_class=HTMLResponse)
async def analisar(text: str = Form(...)):
    payload = {"input_text": text}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        score = data.get("data", {}).get("is_gpt_generated", "desconhecido")
        score_str = f"{score}%" if isinstance(score, (int, float)) else score

        return f"""
            <html>
                <head><title>Resultado</title></head>
                <body>
                    <h2>Resultado da Análise:</h2>
                    <p>Seu texto foi <strong>{score_str}</strong> gerado por IA.</p>
                    <br><a href="/">↩ Voltar</a>
                </body>
            </html>
        """
    except Exception as e:
        return f"""
            <html>
                <body>
                    <h2>Erro</h2>
                    <p>{str(e)}</p>
                    <br><a href="/">↩ Voltar</a>
                </body>
            </html>
        """
