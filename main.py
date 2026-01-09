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

@app.get("/")
def home():
    return {"message": "Server is running"}

# ဒီနေရာကို App က ခေါ်တဲ့ /api/info ဆိုတာနဲ့ ကိုက်အောင် ပြင်လိုက်ပါတယ်
@app.get("/api/info")
async def get_video_info(url: str = Query(...)):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # App က မျှော်လင့်ထားတဲ့ Data format အတိုင်း ပြန်ပေးခြင်း
            return {
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'), # တိုက်ရိုက် download link
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "source": info.get('extractor')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
