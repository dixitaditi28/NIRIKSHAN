import torch
from torch.utils.data import Dataset
import numpy as np
import os
import glob

CACHE_ROOT = r"D:\for_spectrogram_cache"

class ForDataset(Dataset):
    def __init__(self, root_dir, split):
        self.files = []
        self.labels = []

        real_dir = os.path.join(CACHE_ROOT, split, "real")
        fake_dir = os.path.join(CACHE_ROOT, split, "fake")

        real_files = glob.glob(os.path.join(real_dir, "*.npy"))
        fake_files = glob.glob(os.path.join(fake_dir, "*.npy"))

        self.files.extend(real_files)
        self.labels.extend([0] * len(real_files))

        self.files.extend(fake_files)
        self.labels.extend([1] * len(fake_files))

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        filepath = self.files[idx]
        label = self.labels[idx]

        mel_db = np.load(filepath)
        mel_tensor = torch.tensor(mel_db, dtype=torch.float32).unsqueeze(0)
        label_tensor = torch.tensor(label, dtype=torch.long)

        return mel_tensor, label_tensor