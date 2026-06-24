import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time
import winsound
import sqlite3
import time
from datetime import datetime


# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor()

# Drop old table if exists (for development/testing)
cursor.execute("DROP TABLE IF EXISTS emotions")

# Create table with timestamp column
cursor.execute("""
CREATE TABLE emotions (
    emotion TEXT,
    alert TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ---------------- PANIC VARIABLES ----------------
panic_pressed = False
panic_time = 0

# ---------------- LOAD MODEL ----------------
model = load_model("emotion_model.h5")

# ---------------- EMOTION LABELS ----------------
emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

# ---------------- FACE DETECTOR ----------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ---------------- MOUSE CALLBACK ----------------
def mouse_callback(event, x, y, flags, param):
    global panic_pressed, panic_time
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if PANIC button clicked
        if 10 < x < 150 and 10 < y < 50:
            panic_pressed = True
            panic_time = time.time()

# ---------------- WEBCAM SETUP ----------------
cap = cv2.VideoCapture(0)
cv2.namedWindow("Emotion Detection")
cv2.setMouseCallback("Emotion Detection", mouse_callback)

# ---------------- EMOTION HISTORY FOR SMOOTHING ----------------
emotion_history = []

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---------- PANIC BUTTON UI ----------
    cv2.rectangle(frame, (10,10), (150,50), (0,0,255), -1)
    cv2.putText(frame, "PANIC", (30,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "Press P for Panic", (10,460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    # ---------- FACE DETECTION ----------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # -------- FACE PREPROCESSING --------
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48,48))
        face = cv2.cvtColor(face, cv2.COLOR_GRAY2RGB)
        face = face / 255.0
        face = np.reshape(face, (1,48,48,3))

        # -------- PREDICTION --------
        prediction = model.predict(face, verbose=0)
        emotion_index = np.argmax(prediction)
        emotion = emotion_labels[emotion_index]

        # -------- SMOOTHING HISTORY --------
        emotion_history.append(emotion)
        if len(emotion_history) > 10:
            emotion_history.pop(0)
        emotion = max(set(emotion_history), key=emotion_history.count)

        # -------- FEAR PROBABILITY OVERRIDE --------
        fear_prob = prediction[0][2]  # Index 2 corresponds to 'Fear'
        if fear_prob > 0.10:
            emotion = "Fear"

        # -------- ALERT LOGIC --------
        if emotion == "Fear":
            alert = "Alert Sent"
            cv2.putText(frame, "ALERT! CHILD IN FEAR!", (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            winsound.Beep(1000, 500)
        else:
            alert = "No Alert"

        # -------- DRAW FACE AND EMOTION --------
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # -------- STORE IN DATABASE --------
       # Get current local time in IST
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO emotions (emotion, alert, timestamp) VALUES (?, ?, ?)",
               (emotion, alert, timestamp))
        conn.commit()

    # -------- PANIC ALERT LOGIC --------
    if panic_pressed:
        if time.time() - panic_time < 3:
            cv2.putText(frame, "PANIC ALERT!", (50,130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            winsound.Beep(1000, 500)
        else:
            panic_pressed = False

    # -------- DISPLAY FRAME --------
    cv2.imshow("Emotion Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("p"):
        panic_pressed = True
        panic_time = time.time()

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()
conn.close()