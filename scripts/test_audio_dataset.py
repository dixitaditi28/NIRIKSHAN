from audio_dataset import ForDataset

ROOT = r"D:\kagglehub_cache\datasets\mohammedabdeldayem\the-fake-or-real-dataset\versions\2\for-2sec\for-2seconds"

train_data = ForDataset(ROOT, "training")
print("Total training samples:", len(train_data))

mel, label = train_data[0]
print("Mel spectrogram shape:", mel.shape)
print("Label:", label.item())

mel2, label2 = train_data[7000]
print("Second sample shape:", mel2.shape)
print("Second label:", label2.item())