from pathlib import Path
import os
BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

ENCODINGS_PATH = DATA_DIR / "encodings.pkl"

FAISS_INDEX_PATH = DATA_DIR / "faiss.index"

TEMP_DIR = DATA_DIR / "temp"

TEMP_DIR.mkdir(exist_ok=True)

ATTENDANCE_CSV = BASE_DIR / "database" / "attendance.csv"



HF_TOKEN = os.getenv("HF_TOKEN")

HF_API_URL = (
    "https://api-inference.huggingface.co/models/"
    "dima806/facial_emotions_image_detection"
)

FAISS_THRESHOLD = 0.40

CAMERA_INDEX = 0