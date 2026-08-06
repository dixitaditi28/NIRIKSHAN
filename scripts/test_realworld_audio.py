import torch
import torchaudio
import librosa
import numpy as np
import sys
sys.path.append("scripts")
from train_audio_classifier import AudioCNN

SAMPLE_RATE = 16000
N_MELS = 64
FIXED_LENGTH = 63
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


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


def predict(model, filepath, label_name):
    tensor = prepare_clip(filepath).to(DEVICE)
    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)
        pred = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred].item()

    verdict = "REAL" if pred == 0 else "FAKE"
    print(f"{label_name}: predicted = {verdict} (confidence: {confidence:.4f}) | raw probs [real, fake]: {probs[0].tolist()}")


model = AudioCNN().to(DEVICE)
model.load_state_dict(torch.load("models/audio_detection_best_v2.pt", map_location=DEVICE, weights_only=True))
model.eval()

REAL_FILE = r"C:\Users\dixit\Downloads\real-audio-nirikshan.ogg"
FAKE_FILE = r"C:\Users\dixit\Downloads\ttsMP3.com_VoiceText_2026-8-3_17-47-37.mp3"

predict(model, REAL_FILE, "Real recording (you)")
predict(model, FAKE_FILE, "TTS-generated (ttsmp3.com)")