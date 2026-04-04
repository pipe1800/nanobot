import os
import json
import urllib.request
import urllib.error

def ingest_json_file(filepath):
    print(f"Reading {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filepath}")
            return
            
    if not content:
        print("File is empty.")
        return
        
    url = "http://127.0.0.1:8000/memorize"
    headers = {'Content-Type': 'application/json'}
    
    conversation = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and "role" in item and "content" in item:
                role = item["role"]
                text = item["content"]
                if isinstance(text, dict) and "text" in text:
                    text = text["text"]
                elif isinstance(text, list):
                    text = "\n".join([c.get("text", "") for c in text if isinstance(c, dict) and c.get("type") == "text"])
                elif not isinstance(text, str):
                    text = str(text)
                
                conversation.append({
                    "role": role,
                    "content": {"text": text}
                })
    
    if not conversation:
        print(f"Could not extract conversation from {filepath}")
        return
        
    payload = {
        "conversation": conversation,
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
    filepath = "/Users/Pipe/Lumi/linux_sessions/0a3d6cb6-67f7-489b-bfd2-535fd36905ef.json"
    ingest_json_file(filepath)
