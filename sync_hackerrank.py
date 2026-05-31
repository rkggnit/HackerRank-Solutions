import os
import requests
import time

# This now pulls the entire raw cookie string directly
RAW_COOKIE = os.environ.get("HRANK_SESSION")

HEADERS = {
    "Cookie": RAW_COOKIE,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
BASE_URL = "https://www.hackerrank.com/rest/contests/master/submissions"

def sync_hackerrank():
    os.makedirs("HackerRank", exist_ok=True)
    offset = 0
    limit = 20
    
    print("Connecting to HackerRank...")
    while True:
        url = f"{BASE_URL}/?offset={offset}&limit={limit}"
        print(f"Fetching batch from offset {offset}...")
        
        resp = requests.get(url, headers=HEADERS)
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code != 200:
            print("Authorization failed. The session cookie might be expired or incomplete.")
            break
            
        try:
            data = resp.json().get('models', [])
            print(f"Found {len(data)} submissions in this batch.")
        except Exception as e:
            print("Error parsing JSON response.")
            break
            
        if not data:
            print("No more submissions found.")
            break
            
        for sub in data:
            status = sub.get('status')
            slug = sub.get('challenge', {}).get('slug', 'unknown_challenge')
            
            if status == 'Accepted':
                ext = sub.get('language', 'txt')
                file_path = f"HackerRank/{slug}.{ext}"
                
                if os.path.exists(file_path):
                    continue
                    
                print(f"   -> Downloading: {slug}")
                code_resp = requests.get(f"{BASE_URL}/{sub['id']}", headers=HEADERS)
                if code_resp.status_code == 200:
                    code = code_resp.json()['model']['code']
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(code)
                time.sleep(1)
                
        offset += limit

if __name__ == "__main__":
    sync_hackerrank()
