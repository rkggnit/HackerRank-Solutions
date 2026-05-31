#python code to fetch submissions from hackerrank
import os
import requests
import time
import re

# Pull the raw cookie string directly
RAW_COOKIE = os.environ.get("HRANK_SESSION")

HEADERS = {
    "Cookie": RAW_COOKIE,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# Endpoints for Submissions and Challenge details
BASE_SUB_URL = "https://www.hackerrank.com/rest/contests/master/submissions"
BASE_CHAL_URL = "https://www.hackerrank.com/rest/contests/master/challenges"

# Map HackerRank language names to actual file extensions
EXTENSION_MAP = {
    'python': 'py', 'python3': 'py', 'pypy': 'py', 'pypy3': 'py',
    'c': 'c', 'cpp': 'cpp', 'cpp14': 'cpp', 'java': 'java', 'java8': 'java', 'java15': 'java',
    'javascript': 'js', 'node': 'js', 'csharp': 'cs', 'php': 'php',
    'ruby': 'rb', 'go': 'go', 'bash': 'sh', 'sql': 'sql', 'mysql': 'sql', 'oracle': 'sql',
    'rust': 'rs', 'swift': 'swift', 'scala': 'scala'
}

def clean_filename(name):
    # Removes characters that are invalid in Windows/Linux folder names
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def clean_challenge_body(html_content):
    if not html_content:
        return "Description not found."
    
    # 1. Strip out entire <style>...</style> blocks
    html_content = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html_content)
    
    # 2. Strip out entire <script>...</script> blocks
    html_content = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html_content)
    
    # 3. Clean up excessive empty newlines left behind
    html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
    
    return html_content.strip()

def sync_hackerrank():
    os.makedirs("HackerRank", exist_ok=True)
    offset = 0
    limit = 20
    
    print("Connecting to HackerRank...")
    while True:
        url = f"{BASE_SUB_URL}/?offset={offset}&limit={limit}"
        print(f"Fetching batch from offset {offset}...")
        
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print("Authorization failed. The session cookie might be expired or incomplete.")
            break
            
        try:
            data = resp.json().get('models', [])
        except Exception as e:
            print("Error parsing JSON response.")
            break
            
        if not data:
            print("No more submissions found.")
            break
            
        for sub in data:
            status = sub.get('status')
            challenge = sub.get('challenge', {})
            slug = challenge.get('slug', 'unknown_challenge')
            raw_name = challenge.get('name', slug)
            
            if status == 'Accepted':
                clean_name = clean_filename(raw_name)
                lang = sub.get('language', 'txt')
                ext = EXTENSION_MAP.get(lang, lang)
                
                # Create a dedicated folder for this specific problem
                folder_path = os.path.join("HackerRank", clean_name)
                os.makedirs(folder_path, exist_ok=True)
                
                code_file_path = os.path.join(folder_path, f"{clean_name}.{ext}")
                readme_path = os.path.join(folder_path, "README.md")
                
                # If the code already exists, we skip it
                if os.path.exists(code_file_path):
                    continue
                    
                print(f"   -> Downloading Code and Question for: {clean_name}")
                
                # 1. Fetch and save the Code
                code_resp = requests.get(f"{BASE_SUB_URL}/{sub['id']}", headers=HEADERS)
                if code_resp.status_code == 200:
                    code = code_resp.json()['model']['code']
                    with open(code_file_path, "w", encoding="utf-8") as f:
                        f.write(code)
                        
                # 2. Fetch, clean up, and save the Question Details
                chal_resp = requests.get(f"{BASE_CHAL_URL}/{slug}", headers=HEADERS)
                if chal_resp.status_code == 200:
                    chal_data = chal_resp.json().get('model', {})
                    body_html = chal_data.get('body_html', '')
                    
                    # Run the HTML cleaner filter
                    cleaned_body = clean_challenge_body(body_html)
                    
                    readme_content = f"# {raw_name}\n\n{cleaned_body}"
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(readme_content)
                        
                time.sleep(1)
                
        offset += limit

if __name__ == "__main__":
    sync_hackerrank()
