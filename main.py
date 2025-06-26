from fastapi import FastAPI, Form
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
            <head><title>Análise de IA</title></head>
            <body>
                <h2>Cole o texto abaixo:</h2>
                <form method="post">
                    <textarea name="text" rows="20" cols="100" required></textarea><br>
                    <input type="submit" value="Analisar">
                </form>
            </body>
        </html>
    """

# Página de resultado (POST)
@app.post("/", response_class=HTMLResponse)
async def analisar(text: str = Form(...)):
    if not text or len(text.strip()) < 20:
        return """
            <html><body>
            <h2>Erro: texto vazio ou muito curto</h2>
            <p>Verifique se o campo foi realmente preenchido.</p>
            <a href="/">↩ Voltar</a>
            </body></html>
        """

    payload = {"input_text": text}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        score = data.get("data", {}).get("is_gpt_generated", "desconhecido")
        score_str = f"{score}%" if isinstance(score, (int, float)) else score

        return f"""
            <html>
                <head><title>Resultado</title></head>
                <body>
                    <h2>Resultado da Análise:</h2>
                    <p><strong>Seu texto foi {score_str} gerado por IA.</strong></p>
                    <h3>Texto recebido:</h3>
                    <pre>{text}</pre>
                    <br><a href="/">↩ Voltar</a>
                </body>
            </html>
        """

    except requests.exceptions.RequestException as e:
        return f"""
            <html>
                <head><title>Erro</title></head>
                <body>
                    <h2>Erro ao analisar o texto</h2>
                    <p>Talvez o serviço tenha demorado demais para responder.</p>
                    <p><code>{str(e)}</code></p>
                    <a href="/">↩ Voltar</a>
                </body>
            </html>
        """
