import pickle
from pathlib import Path

import cv2
import face_recognition
import faiss
import numpy as np

from config import ENCODINGS_PATH, FAISS_INDEX_PATH

dataset_path = Path("dataset")

known_encodings = []
known_names = []

for person_dir in dataset_path.iterdir():

    if not person_dir.is_dir():
        continue

    person_name = person_dir.name

    for image_path in person_dir.glob("*.*"):

        image = cv2.imread(str(image_path))

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb)

        if len(encodings) > 0:

            known_encodings.append(encodings[0])

            known_names.append(person_name)

print("Encoding completed")

encodings_np = np.array(known_encodings).astype("float32")

index = faiss.IndexFlatL2(128)

index.add(encodings_np)

with open(ENCODINGS_PATH, "wb") as f:

    pickle.dump(
        {
            "encodings": known_encodings,
            "names": known_names,
        },
        f,
    )

faiss.write_index(index, str(FAISS_INDEX_PATH))

print("FAISS index created")