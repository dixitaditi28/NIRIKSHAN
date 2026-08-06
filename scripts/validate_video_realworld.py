import sys
sys.path.insert(0, "scripts")
from video_wrapper import classify_video
import os
from PIL import Image
from video_wrapper import extract_face_frames

os.makedirs("debug_validation_frames", exist_ok=True)

def save_debug_frame(path, label):
    frames = extract_face_frames(path)
    if frames:
        name = path.split('/')[-1].replace('.mp4', '')
        Image.fromarray(frames[0]).save(f"debug_validation_frames/{label}_{name}.jpg")
    else:
        print(f"WARNING: no face detected at all in {path}")

sys.path.insert(0, "scripts")
from video_wrapper import classify_video

real_videos = [
    "D:/ffpp_data/original_sequences/youtube/c23/videos/035.mp4",
    "D:/ffpp_data/original_sequences/youtube/c23/videos/036.mp4",
    "D:/ffpp_data/original_sequences/youtube/c23/videos/924.mp4",
    "D:/ffpp_data/original_sequences/youtube/c23/videos/917.mp4",
    "D:/ffpp_data/original_sequences/youtube/c23/videos/044.mp4",
    "D:/ffpp_data/original_sequences/youtube/c23/videos/945.mp4",
]

fake_videos = [
    "D:/ffpp_data/manipulated_sequences/Deepfakes/c23/videos/035_036.mp4",
    "D:/ffpp_data/manipulated_sequences/Deepfakes/c23/videos/924_917.mp4",
    "D:/ffpp_data/manipulated_sequences/Deepfakes/c23/videos/044_945.mp4",
]

for path in real_videos + fake_videos:
    save_debug_frame(path, "check")

results = []

for path in real_videos:
    r = classify_video(path)
    correct = r["verdict"] == "Real"
    results.append((path, "Real", r["verdict"], r["avg_fake_score"], correct))

for path in fake_videos:
    r = classify_video(path)
    correct = r["verdict"] == "Fake"
    results.append((path, "Fake", r["verdict"], r["avg_fake_score"], correct))

print(f"\n{'Video':<70} {'Expected':<10} {'Predicted':<10} {'AvgScore':<10} {'Correct'}")
for path, expected, predicted, score, correct in results:
    name = path.split('/')[-1]
    print(f"{name:<70} {expected:<10} {predicted:<10} {score:<10.4f} {correct}")

num_correct = sum(1 for r in results if r[4])
total = len(results)
print(f"\nAccuracy: {num_correct}/{total} = {num_correct/total*100:.1f}%")