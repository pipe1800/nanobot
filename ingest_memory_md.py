import os
import json
import urllib.request
import urllib.error

def ingest_memory_file(filepath):
    print(f"Reading {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip():
        print("File is empty.")
        return
        
    url = "http://127.0.0.1:8000/memorize"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "conversation": [
            {"role": "user", "content": f"Here is my long-term memory file containing lessons learned, major decisions, and active projects:\n\n{content}"}
        ],
        "user_id": "Pipe",
        "agent_id": "Lumi"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Success! Task ID: {result.get('result', {}).get('task_id')}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_file = "/Users/Pipe/Lumi/nanobot/lumi_identity/MEMORY.md"
    ingest_memory_file(target_file)
