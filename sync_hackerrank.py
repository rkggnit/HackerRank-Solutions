import os
import requests
import time

HR_COOKIE = os.environ.get("HRANK_SESSION")
# We added a highly realistic User-Agent to prevent HackerRank from blocking the script
HEADERS = {
    "Cookie": f"hrank_session={HR_COOKIE}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
            print("Failed to authenticate. Your HRANK_SESSION cookie might be invalid.")
            break
            
        try:
            data = resp.json().get('models', [])
            print(f"Found {len(data)} submissions in this batch.")
        except Exception as e:
            print("Error parsing JSON. HackerRank might be showing a block page.")
            print(resp.text[:500])
            break
            
        if not data:
            print("No more submissions found. Exiting loop.")
            break
            
        for sub in data:
            status = sub.get('status')
            slug = sub.get('challenge', {}).get('slug', 'unknown_challenge')
            print(f"Checking: {slug} | Status: {status}")
            
            if status == 'Accepted':
                ext = sub.get('language', 'txt')
                file_path = f"HackerRank/{slug}.{ext}"
                
                if os.path.exists(file_path):
                    print(f"   -> Already downloaded, skipping.")
                    continue
                    
                print(f"   -> DOWNLOADING NEW SOLUTION: {slug}")
                code_resp = requests.get(f"{BASE_URL}/{sub['id']}", headers=HEADERS)
                if code_resp.status_code == 200:
                    code = code_resp.json()['model']['code']
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(code)
                time.sleep(1) # Be polite to HackerRank servers
                
        offset += limit

if __name__ == "__main__":
    sync_hackerrank()
