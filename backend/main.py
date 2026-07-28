from fastapi import FastAPI
import chromadb
import re

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import LabelEncoder
import torch

MODEL_PATH = "models/detection/mbert_final"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
text_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
text_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
text_model.eval()

label_encoder = LabelEncoder()
label_encoder.fit(["genuine", "phishing"])

def get_text_risk(text: str) -> float:
    inputs = text_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(device)
    with torch.no_grad():
        outputs = text_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
        phishing_idx = label_encoder.transform(["phishing"])[0]
        return round(probs[phishing_idx].item(), 3)

app = FastAPI(title="NIRIKSHAN Authentication API")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "data/processed/chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection("sebi_circulars")

SEBI_CIRCULAR_PATTERN = re.compile(r"[A-Z]{2,10}/[A-Z0-9]{2,15}/\d{4}[-/]\d{1,4}", re.IGNORECASE)
SEBI_KEYWORD_PATTERN = re.compile(r"\bSEBI\b|\bSecurities and Exchange Board of India\b", re.IGNORECASE)

def claims_sebi_origin(text: str) -> bool:
    has_keyword = bool(SEBI_KEYWORD_PATTERN.search(text))
    has_circular_number = bool(SEBI_CIRCULAR_PATTERN.search(text))
    return has_keyword or has_circular_number

def distance_to_auth_trust(distance: float) -> float:
    MIN_DISTANCE = 0.65
    MAX_DISTANCE = 1.4

    clamped = max(MIN_DISTANCE, min(distance, MAX_DISTANCE))
    normalized = (MAX_DISTANCE - clamped) / (MAX_DISTANCE - MIN_DISTANCE)
    return round(normalized, 3)

@app.get("/")
def read_root():
    return {"status": "NIRIKSHAN API running", "circulars_indexed": collection.count()}

@app.get("/test_text_risk")
def test_text_risk(text: str):
    return {"text": text, "text_risk": get_text_risk(text)}

@app.get("/verify")
def verify_circular(text: str):
    results = collection.query(query_texts=[text], n_results=3)

    matches = []
    for doc, meta, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        matches.append({
            "title": meta["title"],
            "date": meta["date"],
            "distance": distance,
            "auth_trust": distance_to_auth_trust(distance)
        })

    top_auth_trust = matches[0]["auth_trust"] if matches else 0.0

    return {
        "query": text,
        "claims_sebi_origin": claims_sebi_origin(text),
        "top_auth_trust": top_auth_trust,
        "matches": matches
    }
@app.get("/analyze")
def analyze(text: str):
    text_risk = get_text_risk(text)

    chroma_results = collection.query(query_texts=[text], n_results=3)
    matches = []
    for doc, meta, distance in zip(chroma_results["documents"][0], chroma_results["metadatas"][0], chroma_results["distances"][0]):
        matches.append({
            "title": meta["title"],
            "date": meta["date"],
            "distance": distance,
            "auth_trust": distance_to_auth_trust(distance)
        })
    auth_trust = matches[0]["auth_trust"] if matches else 0.0

    sebi_claim = claims_sebi_origin(text)

    trust_score = ((1 - text_risk) * 0.60 + auth_trust * 0.40) * 100

    if text_risk > 0.85:
        trust_score = min(trust_score, 25)
    if sebi_claim and auth_trust < 0.30:
        trust_score = min(trust_score, 35)

    trust_score = round(trust_score, 1)

    if trust_score <= 35:
        band = "High Risk"
    elif trust_score <= 60:
        band = "Medium Risk"
    elif trust_score <= 80:
        band = "Low Risk"
    else:
        band = "Safe"

    return {
        "query": text,
        "text_risk": text_risk,
        "auth_trust": auth_trust,
        "claims_sebi_origin": sebi_claim,
        "trust_score": trust_score,
        "band": band,
        "matches": matches
    }