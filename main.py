from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from translate import Translator  # translate kütüphanesini ekliyoruz

app = FastAPI()

# Static dosyalar için klasör tanımlama
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template klasörünü tanımlama
templates = Jinja2Templates(directory="templates")

# Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )

# Dublaj API endpoint'i
@app.post("/api/dub")
async def create_dubbing(video_id: str, text: str, lang: str = "tr"):
    try:
        # translate kütüphanesi ile çeviri işlemi
        translator = Translator(to_lang=lang)
        translation = translator.translate(text)
        return {"status": "success", "translated_text": translation}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Test endpoint'i
@app.get("/test")
async def test():
    return {"message": "API çalışıyor!"}
