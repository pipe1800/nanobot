import os

files_to_remove = [
    "clean_all_memories.py",
    "clean_memory.py",
    "cleaned_test.json",
    "core_agent_lines.sh",
    "download_identity.py",
    "download_sessions.py",
    "extract_memory.py",
    "generate_embeddings.py",
    "ingest.log",
    "ingest_memories.py",
    "ingest_telegram.py",
    "test_curl.py",
    "test_httpx.py",
    "test_jobbi.py",
    "test_pre_retrieval.py",
    "test_retrieve.py",
    "test_retrieve_3.py",
    "test_retrieve_4.py",
    "test_retrieve_names.py",
    "test_socket.py",
    "test_sse.py",
    "test_urllib.py",
    "update_embeddings.sql"
]

base_dir = "/Users/Pipe/Lumi/nanobot"

for f in files_to_remove:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed {f}")
