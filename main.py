import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime
import pytz

# API anahtarını Render'daki ortam değişkenlerinden al
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"API Anahtarı yapılandırma hatası: {e}")


# Model yapılandırması
generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextData(BaseModel):
    text: str

@app.get("/")
def read_root():
    istanbul_tz = pytz.timezone("Europe/Istanbul")
    now_istanbul = datetime.now(istanbul_tz)
    return {
        "status": "Sentio.ai Gerçek Analiz Motoru Aktif",
        "timestamp": now_istanbul.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/analyze")
async def analyze_text(data: TextData):
    try:
        prompt = f"""
            You are an expert AI text detector. Analyze the following Turkish text.
            Focus on three key metrics:
            1.  **Perplexity:** How diverse and rich is the vocabulary? Is it repetitive?
            2.  **Burstiness:** How varied are the sentence lengths and structures? Is it monotonous or does it have a natural rhythm?
            3.  **Phraseology:** How frequently does it use formal, cliché, or robotic-sounding phrases common in AI generation (like 'bu bağlamda', 'sonuç olarak', 'olanak tanımaktadır')?

            Based on your analysis of these three metrics, provide a JSON object with the following exact structure. Do not add any extra explanations.

            {{
              "overall_score": a float between 0.0 and 1.0 representing the overall probability of the text being AI-generated (where 0.0 is definitely human and 1.0 is definitely AI),
              "comment": a brief Turkish comment based on the score ('Düşük Olasılıkla Yapay Zeka Tarafından Üretilmiş', 'Yapay Zeka Tarafından Üretilmiş Olabilir', or 'Yüksek Olasılıkla Yapay Zeka Tarafından Üretilmiş'),
              "sentences": an array of objects, where each object has "text" (the original sentence) and "ai_score" (a float between 0.0 and 1.0 for that specific sentence).
            }}

            Text to analyze: "{data.text}"
        """

        response = model.generate_content(prompt)

        response_text = response.text.strip().replace("```json", "").replace("```", "").strip()

        return json.loads(response_text)

    except Exception as e:
        print(f"Analiz hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
