from datasets import load_dataset
import soundfile as sf
import os

OUTPUT_DIR = "data/synthetic/audio"
SAMPLE_COUNT = 300

def download_sample():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dataset = load_dataset("LanceaKing/asvspoof2019", split="train", streaming=True)

    bonafide_count = 0
    spoof_count = 0

    for example in dataset:
        label = "bonafide" if example["key"] == 1 else "spoof"
        if label == "bonafide" and bonafide_count >= SAMPLE_COUNT // 2:
            continue
        if label == "spoof" and spoof_count >= SAMPLE_COUNT // 2:
            continue

        filename = f"{label}_{example['audio_file_name']}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)
        sf.write(filepath, example["audio"]["array"], example["audio"]["sampling_rate"])

        if label == "bonafide":
            bonafide_count += 1
        else:
            spoof_count += 1

        if bonafide_count >= SAMPLE_COUNT // 2 and spoof_count >= SAMPLE_COUNT // 2:
            break

    print(f"Downloaded {bonafide_count} bonafide + {spoof_count} spoof samples to {OUTPUT_DIR}")

if __name__ == "__main__":
    download_sample()