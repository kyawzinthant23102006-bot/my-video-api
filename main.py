import yt_dlp
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# App နဲ့ ချိတ်ဆက်မှု ခွင့်ပြုရန်
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# UptimeRobot အတွက် HEAD ရော GET ရော လက်ခံပေးခြင်း
@app.get("/")
@app.head("/")
def home():
    return {"status": "online"}

@app.get("/api/info")
async def get_video_info(url: str = Query(...)):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "source": info.get('extractor')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
