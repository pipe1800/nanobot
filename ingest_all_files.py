import os
import json
import urllib.request
import urllib.error
import time
import glob

def ingest_json_file(filepath):
    print(f"Reading {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filepath}")
            return None
            
    if not content:
        print("File is empty.")
        return None
        
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
        return None
        
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
            task_id = result.get('result', {}).get('task_id')
            print(f"Success! Task ID: {task_id}")
            return task_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_status(task_id):
    url = f"http://127.0.0.1:8000/memorize/status/{task_id}"
    try:
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('result', {}).get('status')
    except Exception as e:
        print(f"Error checking status: {e}")
        return "UNKNOWN"

if __name__ == "__main__":
    directory = "/Users/Pipe/Lumi/linux_sessions"
    processed_file = "0a3d6cb6-67f7-489b-bfd2-535fd36905ef.json"
    
    files = glob.glob(os.path.join(directory, "*.json"))
    files = [f for f in files if not f.endswith(processed_file)]
    
    print(f"Found {len(files)} files to process.")
    
    for i, filepath in enumerate(files):
        print(f"\n--- Processing file {i+1}/{len(files)}: {os.path.basename(filepath)} ---")
        task_id = ingest_json_file(filepath)
        
        if task_id:
            print(f"Waiting for task {task_id} to complete...")
            while True:
                status = check_status(task_id)
                print(f"Status: {status}")
                if status in ["COMPLETED", "FAILED"]:
                    break
                time.sleep(5)
            print(f"Task {task_id} finished with status: {status}")
        else:
            print("Skipping to next file due to error.")
            
        # Small delay between files
        time.sleep(2)
        
    print("\nAll files processed!")
