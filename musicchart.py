import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# .env에서 API 키 로드
load_dotenv()
API_KEY = os.getenv('MUSICAPIKEY')

def get_top_tracks(limit=10):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    }

    response = requests.get(url, params=params)
    print(response.text)  # 🧪 API 응답 내용 확인용 (디버깅 시 중요)

    if response.status_code == 200:
        data = response.json()
        return data.get('tracks', {}).get('track', [])
    else:
        print("❌ API 요청 실패:", response.status_code)
        return []

def save_to_readme(tracks):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("# 🎵 실시간 인기 음악 차트 (Last.fm)\n\n")
        f.write(f"⏰ Updated at: {now}\n\n")
        f.write("## 📈 Top Tracks\n\n")
        
        if not tracks:
            f.write("😢 차트를 불러오지 못했습니다. 나중에 다시 시도해 주세요.\n")
            return

        for i, track in enumerate(tracks, 1):
            name = track['name']
            artist = track['artist']['name']
            url = track['url']
            f.write(f"{i}. [{name} - {artist}]({url})\n")

        f.write("\n---\n*Powered by [Last.fm](https://www.last.fm)*\n")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ API_KEY를 .env에서 불러오지 못했습니다.")
    else:
        top_tracks = get_top_tracks(limit=10)
        save_to_readme(top_tracks)
        print("✅ README.md 업데이트 완료!")