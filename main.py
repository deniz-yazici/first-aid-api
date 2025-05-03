from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
import requests
import json
from io import BytesIO
from PIL import Image

app = FastAPI()

# CORS: Android uygulamadan erişimi sağlar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mapping.json'dan görsel eşleşmeleri yükleniyor
with open("mapping.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

# OpenAI API anahtarını buraya yaz (deneme için)
OPENAI_API_KEY = "sk-XXXXXXX"  # Bunu .env içine alacağız sonra

def call_openai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

def match_image(text: str) -> str:
    text_lower = text.lower()
    for filename, keywords in mapping.items():
        for keyword in keywords.split():
            if keyword in text_lower:
                return f"https://yourdomain.com/animations/{filename}"
    return "https://yourdomain.com/animations/default.gif"

@app.post("/analyze")
def analyze(
    yas: str = Form(...),
    cinsiyet: str = Form(...),
    kaza: str = Form(...),
    semptom: str = Form(...),
    aciklama: str = Form(""),
    gorsel_base64: str = Form("")
):
    prompt = f"{yas} yaşında, {cinsiyet} birey. Kaza: {kaza}. Semptomlar: {semptom}. Açıklama: {aciklama}."

    if gorsel_base64:
        try:
            image_data = base64.b64decode(gorsel_base64)
            image = Image.open(BytesIO(image_data))
            prompt += " Kullanıcı görsel de ekledi."
        except Exception:
            pass

    response = call_openai(prompt)
    animasyon_url = match_image(response)

    return JSONResponse(content={"cevap": response, "animasyon": animasyon_url})
