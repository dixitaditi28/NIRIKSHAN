import cv2
import sys
from transformers import pipeline

FRAME_INTERVAL_SECONDS = 1.0
FAKE_THRESHOLD = 0.5

detector = pipeline(
    "image-classification",
    model="prithivMLmods/deepfake-detector-model-v1"
)

face_detector = cv2.FaceDetectorYN.create("scripts/face_detection_yunet.onnx", "", (320, 320))

def extract_face_frames(video_path, interval_seconds=FRAME_INTERVAL_SECONDS):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0
    frame_interval = max(1, int(round(fps * interval_seconds)))

    face_frames = []
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % frame_interval == 0:
            h_frame, w_frame = frame.shape[:2]
            face_detector.setInputSize((w_frame, h_frame))
            _, faces = face_detector.detect(frame)
            if faces is not None and len(faces) > 0:
                best_face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = int(best_face[0]), int(best_face[1]), int(best_face[2]), int(best_face[3])
                pad = int(0.2 * w)
                x1, y1 = max(0, x - pad), max(0, y - pad)
                x2, y2 = min(frame.shape[1], x + w + pad), min(frame.shape[0], y + h + pad)
                face_crop = frame[y1:y2, x1:x2]
                rgb_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                face_frames.append(rgb_crop)
        frame_index += 1

    cap.release()
    return face_frames

def classify_video(video_path):
    frames = extract_face_frames(video_path)
    if not frames:
        raise ValueError(f"No face frames extracted from {video_path}")

    fake_scores = []
    for frame in frames:
        result = detector(frame)
        fake_entry = next(r for r in result if r["label"].lower() == "fake")
        fake_scores.append(fake_entry["score"])

    avg_fake_score = sum(fake_scores) / len(fake_scores)
    verdict = "Fake" if avg_fake_score >= FAKE_THRESHOLD else "Real"

    return {
        "video_path": video_path,
        "num_frames_analyzed": len(frames),
        "per_frame_fake_scores": fake_scores,
        "avg_fake_score": avg_fake_score,
        "verdict": verdict
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_wrapper.py <path_to_video>")
        sys.exit(1)

    video_path = sys.argv[1]

    import os
    os.makedirs("debug_frames", exist_ok=True)
    from PIL import Image
    debug_frames = extract_face_frames(video_path)
    for i, frame in enumerate(debug_frames[:3]):
        Image.fromarray(frame).save(f"debug_frames/face_frame_{i}.jpg")
    print(f"Saved {min(3, len(debug_frames))} debug face frames to debug_frames/")

    result = classify_video(video_path)
    print(f"\nVideo: {result['video_path']}")
    print(f"Frames analyzed: {result['num_frames_analyzed']}")
    print(f"Per-frame fake scores: {[round(s, 4) for s in result['per_frame_fake_scores']]}")
    print(f"Average fake score: {result['avg_fake_score']:.4f}")
    print(f"Verdict: {result['verdict']}")