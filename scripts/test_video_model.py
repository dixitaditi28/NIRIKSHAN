from transformers import pipeline


detector = pipeline(
    "image-classification",
    model="dima806/deepfake_vs_real_image_detection"
)

result = detector("D:/Projects/NIRIKSHAN/test_images/sample1.jpg")
print(result)