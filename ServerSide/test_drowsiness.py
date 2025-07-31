import cv2
import numpy as np
import mediapipe as mp
import time
from collections import deque

# Mediapipe FaceMesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
drawing = mp.solutions.drawing_utils

# Eye landmark indices for EAR calculation (from Mediapipe's 468 points)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def compute_ear(landmarks, eye_indices, image_width, image_height):
    points = [(int(landmarks[i].x * image_width), int(landmarks[i].y * image_height)) for i in eye_indices]
    A = euclidean(points[1], points[5])
    B = euclidean(points[2], points[4])
    C = euclidean(points[0], points[3])
    ear = (A + B) / (2.0 * C)
    return ear

# EAR threshold and timing
EAR_THRESHOLD = 0.25
DROWSY_TIME_SEC = 2
CONSEC_FRAMES = 0
FPS = 30
MAX_BUFFER = DROWSY_TIME_SEC * FPS

# Smoothing buffer
ear_buffer = deque(maxlen=MAX_BUFFER)

# Start webcam
cap = cv2.VideoCapture(0)
print("[i] Press 'q' to quit.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    status = "No face"
    color = (0, 255, 255)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        left_ear = compute_ear(landmarks, LEFT_EYE, w, h)
        right_ear = compute_ear(landmarks, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2.0

        ear_buffer.append(avg_ear)

        if avg_ear < EAR_THRESHOLD:
            CONSEC_FRAMES += 1
        else:
            CONSEC_FRAMES = 0

        drowsy = CONSEC_FRAMES >= MAX_BUFFER

        status = f"{'DROWSY' if drowsy else 'ALERT'} (EAR: {avg_ear:.2f})"
        color = (0, 0, 255) if drowsy else (0, 255, 0)

    # Overlay status
    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.imshow('EAR-Based Drowsiness Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
