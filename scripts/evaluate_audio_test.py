import torch
import sys
sys.path.append("scripts")
from audio_dataset import ForDataset
from train_audio_classifier import AudioCNN
from torch.utils.data import DataLoader

ROOT = r"D:\kagglehub_cache\datasets\mohammedabdeldayem\the-fake-or-real-dataset\versions\2\for-2sec\for-2seconds"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

test_data = ForDataset(ROOT, "testing")
test_loader = DataLoader(test_data, batch_size=32, shuffle=False, num_workers=0)

model = AudioCNN().to(DEVICE)
model.load_state_dict(torch.load("models/audio_detection_best_v2.pt", map_location=DEVICE))
model.eval()

correct = 0
total = 0
false_positives = 0
false_negatives = 0

with torch.no_grad():
    for mels, labels in test_loader:
        mels, labels = mels.to(DEVICE), labels.to(DEVICE)
        outputs = model(mels)
        preds = torch.argmax(outputs, dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
        false_positives += ((preds == 1) & (labels == 0)).sum().item()
        false_negatives += ((preds == 0) & (labels == 1)).sum().item()

print(f"Test samples: {total}")
print(f"Test accuracy: {correct/total:.4f}")
print(f"False positives (real flagged as fake): {false_positives}")
print(f"False negatives (fake flagged as real): {false_negatives}")