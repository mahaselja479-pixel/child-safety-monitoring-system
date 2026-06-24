# import cv2
# import numpy as np
# import time
# import tkinter as tk
# import threading
# import winsound
# from tensorflow.keras.models import load_model

# # Load model
# model = load_model("emotion_model.h5")
# emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

# # Face detector
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # Variables
# running = False
# panic_pressed = False
# panic_time = 0
# alarm_on = False

# # Start Camera
# def start_camera():
#     global running
#     if not running:
#         running = True
#         status_label.config(text="Status: Running")
#         threading.Thread(target=run_camera).start()

# # Stop Camera
# def stop_camera():
#     global running
#     running = False
#     status_label.config(text="Status: Stopped")

# # Panic Button
# def panic():
#     global panic_pressed, panic_time
#     panic_pressed = True
#     panic_time = time.time()
#     status_label.config(text="Status: PANIC TRIGGERED!")

# # Camera Loop
# def run_camera():
#     global running, panic_pressed, alarm_on

#     cap = cv2.VideoCapture(0)
#     emotion_history = []

#     while running:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#         fear_detected = False

#         for (x, y, w, h) in faces:
#             face = gray[y:y+h, x:x+w]
#             face = cv2.resize(face, (48,48))
#             face = cv2.cvtColor(face, cv2.COLOR_GRAY2RGB)
#             face = face / 255.0
#             face = np.reshape(face, (1,48,48,3))

#             prediction = model.predict(face, verbose=0)
#             emotion_index = np.argmax(prediction)
#             emotion = emotion_labels[emotion_index]

#             # Draw face
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#             cv2.putText(frame, emotion, (x,y-10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)

#             # Fear detection
#             fear_prob = prediction[0][2]
#             if fear_prob > 0.15:
#                 fear_detected = True
#                 cv2.putText(frame,"FEAR DETECTED!",
#                             (50,50),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,(0,0,255),3)

#         # Panic Alert
#         if panic_pressed:
#             if time.time() - panic_time < 3:
#                 cv2.putText(frame,"PANIC ALERT!",
#                             (50,100),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,(0,0,255),3)
#             else:
#                 panic_pressed = False

#         # 🔊 SOUND CONTROL (NO REPEAT)
#         if panic_pressed or fear_detected:
#             if not alarm_on:
#                 winsound.Beep(2000, 800)
#                 alarm_on = True
#         else:
#             alarm_on = False

#         cv2.imshow("Camera", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# # ================= UI =================
# root = tk.Tk()
# root.title("Child Safety System")
# root.geometry("300x250")

# tk.Label(root, text="AI Child Safety System", font=("Arial", 14)).pack(pady=10)

# tk.Button(root, text="Start Camera", command=start_camera,
#           bg="green", fg="white").pack(pady=5)

# tk.Button(root, text="Stop Camera", command=stop_camera,
#           bg="red", fg="white").pack(pady=5)

# tk.Button(root, text="PANIC", command=panic,
#           bg="orange").pack(pady=5)

# status_label = tk.Label(root, text="Status: Idle")
# status_label.pack(pady=10)

# root.mainloop()