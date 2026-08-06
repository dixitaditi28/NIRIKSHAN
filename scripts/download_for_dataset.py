import kagglehub
import time

MAX_RETRIES = 30
WAIT_SECONDS = 5

for attempt in range(1, MAX_RETRIES + 1):
    try:
        path = kagglehub.dataset_download("mohammedabdeldayem/the-fake-or-real-dataset")
        print("Dataset downloaded to:", path)
        break
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt == MAX_RETRIES:
            print("Max retries reached. Giving up.")
            raise
        print(f"Retrying in {WAIT_SECONDS} seconds...")
        time.sleep(WAIT_SECONDS)