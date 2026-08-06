from fastapi import FastAPI, UploadFile, File
import chromadb
import re

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import librosa
import numpy as np
import tempfile

from fastapi.middleware.cors import CORSMiddleware

import os

from fastapi import UploadFile, File
import shutil
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../scripts")
from video_wrapper import classify_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "detection", "mbert_final")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
text_model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
text_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
text_model.eval()

label_encoder = LabelEncoder()
label_encoder.fit(["genuine", "phishing"])
label_encoder = LabelEncoder()
label_encoder.fit(["genuine", "phishing"])

AUDIO_SAMPLE_RATE = 16000
AUDIO_N_MELS = 64
AUDIO_FIXED_LENGTH = 63
AUDIO_MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "audio_detection_best_v2.pt")


class AudioCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


audio_model = AudioCNN().to(device)
audio_model.load_state_dict(torch.load(AUDIO_MODEL_PATH, map_location=device, weights_only=True))
audio_model.eval()


def analyze_audio_file(filepath: str) -> dict:
    audio, sr = librosa.load(filepath, sr=AUDIO_SAMPLE_RATE)

    target_len = AUDIO_SAMPLE_RATE * 2
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=AUDIO_N_MELS)
    mel_db = librosa.power_to_db(mel, ref=np.max)

    if mel_db.shape[1] < AUDIO_FIXED_LENGTH:
        pad_width = AUDIO_FIXED_LENGTH - mel_db.shape[1]
        mel_db = np.pad(mel_db, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mel_db = mel_db[:, :AUDIO_FIXED_LENGTH]

    tensor = torch.tensor(mel_db, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        output = audio_model(tensor)
        probs = torch.softmax(output, dim=1)[0]
        pred = torch.argmax(probs).item()

    return {
        "verdict": "REAL" if pred == 0 else "FAKE",
        "confidence": round(probs[pred].item(), 4),
        "real_probability": round(probs[0].item(), 4),
        "fake_probability": round(probs[1].item(), 4)
    }

def get_text_risk(text: str) -> float:
    inputs = text_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(device)
    with torch.no_grad():
        outputs = text_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
        phishing_idx = label_encoder.transform(["phishing"])[0]
        return round(probs[phishing_idx].item(), 3)

app = FastAPI(title="NIRIKSHAN Authentication API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = os.path.join(BASE_DIR, "..", "data", "processed", "chroma_db")

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection("sebi_circulars")

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
            "auth_trust": distance_to_auth_trust(distance),
            "source_url": meta.get("source_url", "")
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
@app.post("/analyze_audio")
async def analyze_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = analyze_audio_file(tmp_path)
    finally:
        os.remove(tmp_path)

    return {
        "filename": file.filename,
        **result
    }

@app.post("/analyze_video")
async def analyze_video(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = classify_video(temp_path)
    finally:
        os.remove(temp_path)

    return {
        "filename": file.filename,
        "num_frames_analyzed": result["num_frames_analyzed"],
        "avg_fake_score": result["avg_fake_score"],
        "verdict": result["verdict"]
    }

from backend.whatsapp_bot import router as whatsapp_router
app.include_router(whatsapp_router)