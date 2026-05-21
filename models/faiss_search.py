import faiss
import pickle
import numpy as np

from config import (
    ENCODINGS_PATH,
    FAISS_INDEX_PATH,
    FAISS_THRESHOLD,
)

with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

names = data["names"]

index = faiss.read_index(str(FAISS_INDEX_PATH))


def recognize_face(face_encoding):

    query = np.array(
        [face_encoding],
        dtype=np.float32,
    )

    distances, indices = index.search(query, 1)

    best_distance = distances[0][0]
    best_index = indices[0][0]

    print("Distance:", best_distance)

    if best_distance < FAISS_THRESHOLD:

        return names[best_index]

    return "Unknown"