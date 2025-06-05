import requests
from data import db
import json
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def search_youtube(query: str, max_results=3) -> list:
    """Search YouTube for educational videos."""
    if not YOUTUBE_API_KEY:
        print("[YouTube API error] YOUTUBE_API_KEY not set in .env")
        return []
    SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY
    }
    try:
        resp = requests.get(SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get('items', [])
        results = [
            {
                'title': item['snippet']['title'],
                'url': f"https://youtube.com/watch?v={item['id']['videoId']}"
            } for item in items
        ]
        return results
    except Exception as e:
        print(f"[YouTube API error] {e}")
        return []

def search_wikipedia(query: str) -> list:
    """Search Wikipedia for concept explanations."""
    SEARCH_URL = f'https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(" ", "%20")}'
    try:
        resp = requests.get(SEARCH_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return [{
                'title': data.get('title'),
                'url': data.get('content_urls', {}).get('desktop', {}).get('page'),
                'extract': data.get('extract')
            }]
        return []
    except Exception as e:
        print(f"[Wikipedia API error] {e}")
        return []

def search_pdfs(query: str, max_results=1) -> list:
    """
    Return a Google search link for PDFs related to the query.
    """
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+filetype:pdf"
    return [{
        'title': f"Search Google for PDFs about '{query}'",
        'url': search_url
    }]

def add_resource_to_db(path_id: int, title: str, url: str, type_: str, difficulty: str = None):
    """Add a resource to the database."""
    conn = db.get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO resources (path_id, title, url, type, difficulty) VALUES (?, ?, ?, ?, ?)",
        (path_id, title, url, type_, difficulty)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("YouTube results:", search_youtube("python tutorial"))
    print("Wikipedia results:", search_wikipedia("Python (programming language)")) 