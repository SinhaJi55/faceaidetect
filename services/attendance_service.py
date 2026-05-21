import csv
from datetime import datetime

from config import ATTENDANCE_CSV


def save_attendance(name, emotion):

    now = datetime.now()

    file_exists = ATTENDANCE_CSV.exists()

    with open(ATTENDANCE_CSV, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow(
                [
                    "Name",
                    "Emotion",
                    "Date",
                    "Time",
                ]
            )

        writer.writerow(
            [
                name,
                emotion,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
            ]
        )