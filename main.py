import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime
import pytz
import re

# API anahtarını Render'daki ortam değişkenlerinden al
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"API Anahtarı yapılandırma hatası: {e}")

# Model yapılandırması - Daha deterministik
generation_config = {
    "temperature": 0.1,  # Daha düşük temperature
    "top_p": 0.8,        # Daha düşük top_p
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

def preprocess_text(text):
    """Metni analiz için temizle ve hazırla"""
    # Gereksiz boşlukları temizle
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def create_advanced_prompt(text):
    """Türkçe için optimize edilmiş gelişmiş prompt"""
    
    return f"""
SEN BİR TÜRKÇE DİLBİLİMSEL ANALİZ UZMANISINN. Görvevin, verilen Türkçe metnin insan tarafından mı yoksa yapay zeka tarafından mı yazıldığını yüksek doğrulukla tespit etmek.

TÜRKÇE'YE ÖZEL ANALİZ KRİTERLERİ:

1. PERPLEXITY (Kelime Zenginliği):
   ✅ İNSAN BELİRTİLERİ: Zengin kelime çeşitliliği, beklenmedik kelime seçimleri, Türkçe'nin doğal eklimeli yapısından yararlanma
   ❌ AI BELİRTİLERİ: Tekrarlayan kelimeler, monoton kelime kullanımı, sınırlı kelime dağarcığı

2. BURSTINESS (Cümle Ritmi):
   ✅ İNSAN BELİRTİLERİ: Değişken cümle uzunlukları, kısa-uzun cümle karışımı, doğal akış
   ❌ AI BELİRTİLERİ: Tekdüze cümle yapıları, monoton ritim, makine benzeri düzenlilik

3. PHRASEOLOGY (Kalıplaşmış Dil):
   ❌ YÜKSEK AI SKORU VER: "bu bağlamda", "kapsamlı bir şekilde", "olanak tanımaktadır", "söz konusu", "nitekim", "bu doğrultuda", "sistematik bir yaklaşım", "entegrasyon süreci", "optimize etmek", "çerçevesinde"
   ✅ DÜŞÜK AI SKORU VER: Günlük dil, kişisel deneyimler, duygusal ifadeler, özgün anlatım

4. TÜRKÇE AKADEMİK DİL ÖZELLİKLERİ:
   ❌ AI KALIPLARI: Aşırı resmi ton, robot benzeri akademik jargon, sürekli pasif cümleler
   ✅ İNSAN ÖZELLİKLERİ: Doğal akademik dil, aktif-pasif karışımı, özgün ifadeler

SKOR VERME KURALLARI:
- Eğer metin AI kalıplarıyla DOLU ise → 0.80-1.00 arası skor ver
- Eğer metin kısmen AI kalıpları içeriyorsa → 0.40-0.79 arası skor ver  
- Eğer metin doğal ve insan benzeri ise → 0.00-0.39 arası skor ver

ANALİZ EDİLECEK METİN:
"{text}"

ÇIKTI FORMATI (SADECE JSON DÖNDÜR):
{{
  "overall_score": [0.00-1.00 arası kesin float değer],
  "comment": "[Türkçe yorum]",
  "sentences": [
    {{"text": "[cümle]", "ai_score": [0.00-1.00 arası float]}},
    {{"text": "[cümle]", "ai_score": [0.00-1.00 arası float]}}
  ]
}}

YORUM REHBERİ:
- 0.00-0.20: "Kesinlikle İnsan Tarafından Yazılmış"
- 0.21-0.40: "Büyük Olasılıkla İnsan Tarafından Yazılmış" 
- 0.41-0.60: "Belirsiz - Karma İçerik"
- 0.61-0.80: "Büyük Olasılıkla Yapay Zeka Tarafından Üretilmiş"
- 0.81-1.00: "Kesinlikle Yapay Zeka Tarafından Üretilmiş"

DİKKAT: Sadece JSON döndür, başka hiçbir metin ekleme!
"""

@app.get("/")
def read_root():
    istanbul_tz = pytz.timezone("Europe/Istanbul")
    now_istanbul = datetime.now(istanbul_tz)
    return {
        "status": "Sentio.ai Gelişmiş Analiz Motoru v2.0 Aktif",
        "timestamp": now_istanbul.strftime("%Y-%m-%d %H:%M:%S"),
        "optimization": "Türkçe dilbilimsel analiz optimize edildi"
    }

@app.post("/analyze")
async def analyze_text(data: TextData):
    try:
        # Metni ön işlemden geçir
        processed_text = preprocess_text(data.text)
        
        if len(processed_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Metin çok kısa, en az 10 karakter gerekli")
        
        # Gelişmiş prompt oluştur
        prompt = create_advanced_prompt(processed_text)
        
        # Model ile analiz yap
        response = model.generate_content(prompt)
        
        # Response'u temizle
        response_text = response.text.strip()
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        response_text = response_text.strip()
        
        # JSON parse et
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Hatası: {e}")
            print(f"Raw Response: {response_text}")
            raise HTTPException(status_code=500, detail="API yanıtı geçersiz JSON formatında")
        
        # Cümleleri otomatik böl ve skoru hesapla
        if "sentences" not in result or not result["sentences"]:
            sentences = re.split(r'[.!?]+', processed_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            result["sentences"] = []
            for sentence in sentences:
                if sentence:
                    # Her cümle için basit AI skorlama
                    ai_phrases = ["bu bağlamda", "kapsamlı", "sistematik", "entegrasyon", "optimize"]
                    ai_score = min(0.9, sum(0.2 for phrase in ai_phrases if phrase in sentence.lower()))
                    result["sentences"].append({
                        "text": sentence + ".",
                        "ai_score": max(0.1, ai_score)
                    })
        
        # Skor validasyonu
        if not (0.0 <= result.get("overall_score", -1) <= 1.0):
            result["overall_score"] = 0.5  # Default safe value
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analiz hatası: {e}")
        print(f"Metin uzunluğu: {len(data.text)}")
        raise HTTPException(status_code=500, detail=f"Analiz işlemi başarısız: {str(e)}")

# Debug endpoint
@app.post("/debug-analyze")
async def debug_analyze(data: TextData):
    """Debug için ham response döndürür"""
    try:
        processed_text = preprocess_text(data.text)
        prompt = create_advanced_prompt(processed_text)
        response = model.generate_content(prompt)
        
        return {
            "raw_response": response.text,
            "processed_text": processed_text,
            "prompt_length": len(prompt)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
