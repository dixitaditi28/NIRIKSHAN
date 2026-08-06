import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import sys
sys.path.append("scripts")
from audio_dataset import ForDataset

ROOT = r"D:\kagglehub_cache\datasets\mohammedabdeldayem\the-fake-or-real-dataset\versions\2\for-2sec\for-2seconds"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001


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


def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for mels, labels in loader:
            mels, labels = mels.to(DEVICE), labels.to(DEVICE)
            outputs = model(mels)
            preds = torch.argmax(outputs, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total


def main():
    print("Loading datasets...")
    train_data = ForDataset(ROOT, "training")
    val_data = ForDataset(ROOT, "validation")

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print("Training samples:", len(train_data))
    print("Validation samples:", len(val_data))

    model = AudioCNN().to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        model.train()
        running_loss = 0.0

        for mels, labels in train_loader:
            mels, labels = mels.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(mels)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        val_acc = evaluate(model, val_loader)
        avg_loss = running_loss / len(train_loader)

        print(f"Epoch {epoch}/{EPOCHS} - Train Loss: {avg_loss:.4f} - Val Accuracy: {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), "models/audio_detection_best_v2.pt")
            print(f"  -> New best model saved (val acc: {val_acc:.4f})")

    print("Training complete. Best validation accuracy:", best_val_acc)


if __name__ == "__main__":
    main()