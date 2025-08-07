from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Tarayıcıların sunucuya erişmesine izin vermek için gerekli ayarlar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Herkese açık
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Sentio.ai Analiz Sunucusu Aktif"}

# Gelecekte analiz fonksiyonumuz buraya eklenecek
# @app.post("/analyze")
# def analyze_text(data: dict):
#     text = data.get("text")
#     # ... model analizi burada yapılacak ...
#     return {"result": "analiz sonucu"}
