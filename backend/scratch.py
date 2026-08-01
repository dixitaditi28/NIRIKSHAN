import chromadb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = client.list_collections()
print(f"Found {len(collections)} collection(s):")
for c in collections:
    print(f" - {c.name}: {client.get_collection(c.name).count()} documents")