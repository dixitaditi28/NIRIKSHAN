import torch
import librosa
import numpy as np
import glob
import os
import sys
sys.path.append("scripts")
from train_audio_classifier import AudioCNN

SAMPLE_RATE = 16000
N_MELS = 64
FIXED_LENGTH = 63
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

REAL_DIR = r"D:\audio_validation_set\real"
FAKE_DIR = r"D:\audio_validation_set\fake"


def prepare_clip(filepath):
    audio, sr = librosa.load(filepath, sr=SAMPLE_RATE)

    target_len = SAMPLE_RATE * 2
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=N_MELS)
    mel_db = librosa.power_to_db(mel, ref=np.max)

    if mel_db.shape[1] < FIXED_LENGTH:
        pad_width = FIXED_LENGTH - mel_db.shape[1]
        mel_db = np.pad(mel_db, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mel_db = mel_db[:, :FIXED_LENGTH]

    tensor = torch.tensor(mel_db, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    return tensor


def predict(model, filepath):
    tensor = prepare_clip(filepath).to(DEVICE)
    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)[0]
        pred = torch.argmax(probs).item()
    return pred, probs[pred].item()


def run_validation():
    model = AudioCNN().to(DEVICE)
    model.load_state_dict(torch.load("models/audio_detection_best_v2.pt", map_location=DEVICE, weights_only=True))
    model.eval()

    real_files = glob.glob(os.path.join(REAL_DIR, "*"))
    fake_files = glob.glob(os.path.join(FAKE_DIR, "*"))

    correct = 0
    total = 0
    results = []

    print(f"\n{'='*60}")
    print("REAL VOICE SAMPLES (expected: REAL)")
    print(f"{'='*60}")
    for f in real_files:
        try:
            pred, conf = predict(model, f)
            verdict = "REAL" if pred == 0 else "FAKE"
            is_correct = (pred == 0)
            correct += is_correct
            total += 1
            mark = "✓" if is_correct else "✗ WRONG"
            print(f"{mark}  {os.path.basename(f):50s} -> {verdict} ({conf*100:.1f}%)")
        except Exception as e:
            print(f"FAILED to process {f}: {e}")

    print(f"\n{'='*60}")
    print("FAKE/SYNTHETIC SAMPLES (expected: FAKE)")
    print(f"{'='*60}")
    for f in fake_files:
        try:
            pred, conf = predict(model, f)
            verdict = "REAL" if pred == 0 else "FAKE"
            is_correct = (pred == 1)
            correct += is_correct
            total += 1
            mark = "✓" if is_correct else "✗ WRONG"
            print(f"{mark}  {os.path.basename(f):50s} -> {verdict} ({conf*100:.1f}%)")
        except Exception as e:
            print(f"FAILED to process {f}: {e}")

    print(f"\n{'='*60}")
    print(f"TOTAL: {correct}/{total} correct ({(correct/total*100 if total else 0):.1f}%)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_validation()