import json
import os
import chromadb

INPUT_FILE = "data/processed/circulars.json"
CHROMA_DIR = "data/processed/chroma_db"

def build_embeddings():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        circulars = json.load(f)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection("sebi_circulars")

    documents = []
    metadatas = []
    ids = []

    for i, c in enumerate(circulars):
        title = c.get("title", "")
        preview = (c.get("full_text") or "")[:300]
        combined_text = f"{title}. {preview}"

        documents.append(combined_text)
        metadatas.append({
            "title": title,
            "date": c.get("date", ""),
            "source_url": c.get("page_url", ""),
            "pdf_url": c.get("pdf_url", "")
        })
        ids.append(f"circular_{i}")

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Added {len(documents)} circulars to ChromaDB collection.")

def test_query(query_text, n_results=3):
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection("sebi_circulars")
    results = collection.query(query_texts=[query_text], n_results=n_results)

    for doc, meta, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        print(f"\nMatch (distance={distance:.4f}):")
        print(f"Title: {meta['title']}")
        print(f"Date: {meta['date']}")

if __name__ == "__main__":
    build_embeddings()
    print("\n--- Test query ---")
    test_query("Ease of Doing Investment framework for transmission of securities")