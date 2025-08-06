import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# 1. .env 파일에서 API_KEY 로드
load_dotenv()
API_KEY = os.getenv('MUSICAPIKEY')

# 2. 차트 가져오기
def get_top_tracks(limit=10):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['tracks']['track']
    else:
        print("❌ API 요청 실패:", response.status_code)
        return []

# 3. README.md에 쓰기
def save_to_readme(tracks):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("# 🎵 실시간 인기 음악 차트 (Last.fm)\n\n")
        f.write(f"⏰ Updated at: {now}\n\n")
        f.write("## 📈 Top Tracks\n\n")
        for i, track in enumerate(tracks, 1):
            name = track['name']
            artist = track['artist']['name']
            url = track['url']
            f.write(f"{i}. [{name} - {artist}]({url})\n")
        f.write("\n---\n*Powered by [Last.fm](https://www.last.fm)*\n")

# 4. 실행
if __name__ == "__main__":
    if not MUSICAPIKEY:
        print("❌ .env 파일에서 API_KEY를 찾을 수 없습니다.")
    else:
        top_tracks = get_top_tracks(limit=10)
        save_to_readme(top_tracks)
        print("✅ README.md 업데이트 완료!")