import os
import requests
import time

# Retrieve the secure cookie from GitHub Secrets
HR_COOKIE = os.environ.get("HRANK_SESSION")
HEADERS = {
    "Cookie": f"hrank_session={HR_COOKIE}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
BASE_URL = "https://www.hackerrank.com/rest/contests/master/submissions"

def sync_hackerrank():
    # Create the target folder if it doesn't exist
    os.makedirs("HackerRank", exist_ok=True)
    offset = 0
    limit = 50
    
    print("Connecting to HackerRank...")
    while True:
        # Fetch a batch of recent submissions
        resp = requests.get(f"{BASE_URL}/?offset={offset}&limit={limit}", headers=HEADERS)
        if resp.status_code != 200:
            print("Failed to authenticate. Please check your HRANK_SESSION secret.")
            break
            
        data = resp.json().get('models', [])
        if not data:
            break
            
        for sub in data:
            if sub['status'] == 'Accepted':
                slug = sub['challenge']['slug']
                ext = sub['language']
                file_path = f"HackerRank/{slug}.{ext}"
                
                # Skip if we already downloaded this solution to avoid API spam
                if os.path.exists(file_path):
                    continue
                    
                print(f"Fetching new accepted solution: {slug}")
                # Fetch the actual code for this specific submission ID
                code_resp = requests.get(f"{BASE_URL}/{sub['id']}", headers=HEADERS)
                if code_resp.status_code == 200:
                    code = code_resp.json()['model']['code']
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(code)
                
                # Pause briefly to respect rate limits
                time.sleep(1) 
                
        offset += limit

if __name__ == "__main__":
    sync_hackerrank()
