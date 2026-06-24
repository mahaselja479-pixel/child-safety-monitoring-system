import cv2

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Read frame from webcam
    
    if not ret:
        break

    cv2.imshow("Webcam", frame)  # Show the frame

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()