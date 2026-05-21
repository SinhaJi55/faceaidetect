from datetime import datetime
import time
from collections import defaultdict

import cv2
import face_recognition
from PIL import Image, ImageTk

from api.huggingface_api import detect_emotion
from config import CAMERA_INDEX, TEMP_DIR
from models.faiss_search import recognize_face
from services.attendance_service import save_attendance
from ui.dashboard import Dashboard


# -----------------------------
# App UI
# -----------------------------

app = Dashboard()

cap = cv2.VideoCapture(CAMERA_INDEX)

marked = set()

# -----------------------------
# Emotion API Optimization
# -----------------------------

last_emotion = "Neutral"

processed_people = {}

API_INTERVAL = 5

# -----------------------------
# Stable Face Recognition
# -----------------------------

detection_count = defaultdict(int)

CONFIRM_FRAMES = 5


def update():

    global last_emotion

    ret, frame = cap.read()

    if ret:

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        faces = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(
            rgb,
            faces,
        )

        for encoding, face in zip(encodings, faces):

            top, right, bottom, left = face

            # -----------------------------
            # Face Recognition
            # -----------------------------

            predicted_name = recognize_face(encoding)

            detection_count[predicted_name] += 1

            if detection_count[predicted_name] >= CONFIRM_FRAMES:

                name = predicted_name

            else:

                name = "Detecting..."

            # -----------------------------
            # Emotion Detection
            # -----------------------------

            face_crop = frame[top:bottom, left:right]

            emotion = last_emotion

            current_time = time.time()

            should_call_api = (
                name != "Unknown"
                and name != "Detecting..."
                and (
                    name not in processed_people
                    or current_time - processed_people[name] > API_INTERVAL
                )
            )

            if face_crop.size > 0 and should_call_api:

                temp_path = TEMP_DIR / "temp.jpg"

                cv2.imwrite(
                    str(temp_path),
                    face_crop,
                )

                try:

                    emotion = detect_emotion(temp_path)

                    last_emotion = emotion

                    processed_people[name] = current_time

                except Exception as e:

                    print("HuggingFace API Failed:", e)

                    emotion = "Neutral"

            # -----------------------------
            # Draw Face Box
            # -----------------------------

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"{name} | {emotion}",
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            # -----------------------------
            # Attendance
            # -----------------------------

            if (
                name != "Unknown"
                and name != "Detecting..."
            ):

                if name not in marked:

                    marked.add(name)

                    app.counter.configure(
                        text=str(len(marked))
                    )

                    now = datetime.now()

                    app.tree.insert(
                        "",
                        "end",
                        values=(
                            name,
                            emotion,
                            now.strftime("%Y-%m-%d"),
                            now.strftime("%H:%M:%S"),
                        ),
                    )

                    save_attendance(
                        name,
                        emotion,
                    )

        # -----------------------------
        # Show Webcam
        # -----------------------------

        image = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        image = Image.fromarray(image)

        image_tk = ImageTk.PhotoImage(image=image)

        app.video_label.configure(
            image=image_tk,
        )

        app.video_label.image = image_tk

    app.after(10, update)


update()

app.mainloop()