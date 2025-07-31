from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import cv2
import numpy as np
import mediapipe as mp
from io import BytesIO

app = Flask(__name__)

# Optional: enable CORS if your frontend is served from a different origin
CORS(app)

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# EAR landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def compute_ear(landmarks, eye_indices, width, height):
    points = [
        (int(landmarks[i].x * width), int(landmarks[i].y * height))
        for i in eye_indices
    ]
    A = euclidean(points[1], points[5])
    B = euclidean(points[2], points[4])
    C = euclidean(points[0], points[3])
    return (A + B) / (2.0 * C)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Drowsiness Detection API"}), 200

@app.route('/detect', methods=['POST'])
def detect():
    try:
        # 1) Read image bytes
        img_bytes = BytesIO(request.data).read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "invalid image"}), 400

        # 2) Run FaceMesh
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return jsonify({"error": "no face detected"}), 200

        # 3) Compute EAR
        landmarks = result.multi_face_landmarks[0].landmark
        left_ear  = compute_ear(landmarks, LEFT_EYE,  w, h)
        right_ear = compute_ear(landmarks, RIGHT_EYE, w, h)
        avg_ear   = (left_ear + right_ear) / 2.0

        # 4) Determine drowsiness
        DROWSY_THRESHOLD = 0.25
        drowsy_np = avg_ear < DROWSY_THRESHOLD
        drowsy = bool(drowsy_np)  # convert numpy.bool_ to native bool

        # 5) Return JSON
        return jsonify({
            "drowsy": drowsy,
            "confidence": round(avg_ear, 3)
        })

    except Exception as e:
        print("[ERROR] in /detect:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
