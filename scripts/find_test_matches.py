import json
import os

with open("D:/Projects/NIRIKSHAN/data/ffpp_splits/test.json") as f:
    test_pairs = json.load(f)

test_ids = set()
for pair in test_pairs:
    test_ids.update(pair)

originals_dir = "D:/ffpp_data/original_sequences/youtube/c23/videos"
deepfakes_dir = "D:/ffpp_data/manipulated_sequences/Deepfakes/c23/videos"

downloaded_originals = {f.replace(".mp4", "") for f in os.listdir(originals_dir) if f.endswith(".mp4")}
downloaded_deepfakes = {f.replace(".mp4", "") for f in os.listdir(deepfakes_dir) if f.endswith(".mp4")}

matched_originals = downloaded_originals & test_ids
print(f"Downloaded originals matching test.json: {sorted(matched_originals)}")

matched_pairs = []
for pair in test_pairs:
    target, source = pair
    combo = f"{target}_{source}"
    if combo in downloaded_deepfakes:
        matched_pairs.append(combo)
print(f"Downloaded Deepfakes matching test.json pairs: {matched_pairs}")