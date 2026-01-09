import yt_dlp
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# App နဲ့ ချိတ်ဆက်မှု ခွင့်ပြုရန် (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Server is running"}

# App က /api/info ကို လှမ်းခေါ်နေတာကြောင့် ဒါကို ပြင်လိုက်တာပါ
@app.get("/api/info")
async def get_video_info(url: str = Query(...)):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video အချက်အလက်များကို ဆွဲထုတ်ခြင်း
            info = ydl.extract_info(url, download=False)
            
            # App က မျှော်လင့်ထားတဲ့ JSON format အတိုင်း ပြန်ပေးခြင်း
            return {
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'), # Direct video link
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "source": info.get('extractor')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
