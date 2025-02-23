import cv2
import numpy as np
import pandas as pd
from pyzbar.pyzbar import decode
from datetime import datetime

# Initialize DataFrame for attendance
df = pd.DataFrame(columns=["Student Name", "Date", "Time"])


def scan_qr():
    cap = cv2.VideoCapture(0)
    global df

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for qr_code in decode(frame):
            qr_data = qr_code.data.decode('utf-8')
            pts = np.array([qr_code.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            current_time = datetime.now()
            date = current_time.strftime("%Y-%m-%d")
            time = current_time.strftime("%H:%M:%S")

            if qr_data not in df["Student Name"].values:
                df = pd.concat([df, pd.DataFrame([[qr_data, date, time]], columns=df.columns)], ignore_index=True)
                print(f"Recorded: {qr_data} at {time} on {date}")

            cv2.putText(frame, qr_data, (qr_code.rect.left, qr_code.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    save_to_excel()


def save_to_excel():
    df.to_excel("attendance.xlsx", index=False)
    print("Attendance Record Saved to attendance.xlsx")


if __name__ == "__main__":
    print("Starting QR Code Attendance System...")
    scan_qr()
