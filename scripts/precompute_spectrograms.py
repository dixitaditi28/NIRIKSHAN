import numpy as np
import librosa
import glob
import os
import io
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
import time

SAMPLE_RATE = 16000
N_MELS = 64
FIXED_LENGTH = 63
ROOT = r"D:\kagglehub_cache\datasets\mohammedabdeldayem\the-fake-or-real-dataset\versions\2\for-2sec\for-2seconds"
CACHE_ROOT = r"D:\for_spectrogram_cache"


def mp3_roundtrip(audio, sr):
    audio_int16 = (audio * 32767).astype(np.int16)
    segment = AudioSegment(audio_int16.tobytes(), frame_rate=sr, sample_width=2, channels=1)

    buffer = io.BytesIO()
    segment.export(buffer, format="mp3", bitrate="64k")
    buffer.seek(0)

    decoded = AudioSegment.from_file(buffer, format="mp3")
    decoded = decoded.set_frame_rate(sr).set_channels(1)

    samples = np.array(decoded.get_array_of_samples()).astype(np.float32) / 32767.0

    if len(samples) < len(audio):
        samples = np.pad(samples, (0, len(audio) - len(samples)))
    else:
        samples = samples[:len(audio)]

    return samples


def process_one(args):
    filepath, out_path = args
    if os.path.exists(out_path):
        return "skipped"

    try:
        audio, sr = librosa.load(filepath, sr=SAMPLE_RATE)
        audio = mp3_roundtrip(audio, sr)

        mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=N_MELS)
        mel_db = librosa.power_to_db(mel, ref=np.max)

        if mel_db.shape[1] < FIXED_LENGTH:
            pad_width = FIXED_LENGTH - mel_db.shape[1]
            mel_db = np.pad(mel_db, ((0, 0), (0, pad_width)), mode="constant")
        else:
            mel_db = mel_db[:, :FIXED_LENGTH]

        np.save(out_path, mel_db.astype(np.float32))
        return "ok"
    except Exception as e:
        return f"FAILED: {filepath} -> {e}"


def build_job_list():
    jobs = []
    for split in ["training", "validation", "testing"]:
        for label in ["real", "fake"]:
            src_dir = os.path.join(ROOT, split, label)
            out_dir = os.path.join(CACHE_ROOT, split, label)
            os.makedirs(out_dir, exist_ok=True)

            files = glob.glob(os.path.join(src_dir, "*.wav"))
            for f in files:
                fname = os.path.basename(f) + ".npy"
                out_path = os.path.join(out_dir, fname)
                jobs.append((f, out_path))
    return jobs


if __name__ == "__main__":
    jobs = build_job_list()
    print(f"Total files to process: {len(jobs)}")

    start = time.time()
    done = 0
    failed = []

    with ProcessPoolExecutor(max_workers=8) as executor:
        for result in executor.map(process_one, jobs, chunksize=20):
            done += 1
            if result.startswith("FAILED"):
                failed.append(result)
            if done % 500 == 0:
                elapsed = time.time() - start
                print(f"Processed {done}/{len(jobs)} - elapsed {elapsed:.0f}s")

    print(f"Done. Total time: {time.time()-start:.0f}s")
    print(f"Failures: {len(failed)}")
    for f in failed[:10]:
        print(f)