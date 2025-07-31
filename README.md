# 🛌 Vigilant Eye Cam – Real-Time Drowsiness Detection

**Vigilant Eye Cam** is a real-time drowsiness detection system built with **React (TypeScript)** on the frontend and a **Flask (Python)** backend. It uses a webcam to monitor a user's face and detect signs of drowsiness using a pre-trained deep learning model. If drowsiness is detected, an alarm is triggered, and a visual warning is displayed.

---

## 🚀 Features

* 🎥 **Live Webcam Feed** – Automatically detects and streams the user's webcam.
* 🧠 **ML-Based Drowsiness Detection** – Sends frames to a Flask backend with a TensorFlow model for analysis.
* 🔔 **Real-Time Alert System** – Shows warning banners and plays an alarm if drowsiness is detected.
* 🧪 **Retry Logic** – Automatically retries failed detection requests.
* 🖥️ **Mobile-Responsive UI** – Built with Tailwind CSS and React components.
* 🔇 **Toggleable Alarm** – Easily enable or disable the alarm sound.

---

## 📁 Project Structure

```
vigilant-eye-cam/
│
├── frontend/                # React + TypeScript app
│   └── src/
│       └── components/
│           └── DrowsinessDetector.tsx
│
├── backend/                 # Flask backend
│   ├── app.py
│   └── drowsiness_model.h5
│
├── public/
├── README.md
```

---

## 🧠 How It Works

1. The frontend captures a frame every second from the webcam.
2. Each frame is sent as a JPEG image to the Flask backend.
3. The backend loads a pre-trained Keras model (`drowsiness_model.h5`) to analyze the image.
4. The backend responds with:

   ```json
   { "drowsy": true, "confidence": 0.92 }
   ```
5. If `drowsy` is `true`, the UI shows a warning banner and triggers an alarm.

---

## 🔧 Setup Instructions

### 1. Backend (Python + Flask)

#### 📦 Requirements

* Python 3.7+
* TensorFlow
* Flask
* OpenCV
* NumPy

#### 🛠 Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Sample `requirements.txt`:**

```txt
Flask
tensorflow
opencv-python
numpy
flask-cors
```

#### 🧠 Start the Backend Server

```bash
python app.py
```

> Ensure `drowsiness_model.h5` exists in the backend folder.

---

### 2. Frontend (React + Vite + Tailwind)

#### 📦 Requirements

* Node.js 18+
* npm or yarn

#### 🛠 Install and Start

```bash
cd frontend
npm install
npm run dev
```

> The frontend runs on `http://localhost:5173` and expects the backend at `http://localhost:5000`.

---

## 📱 API Endpoint

### POST `/detect`

* **Headers**: `Content-Type: image/jpeg`
* **Body**: JPEG image blob
* **Response**:

  ```json
  {
    "drowsy": true,
    "confidence": 0.87
  }
  ```

---

## ⚙️ Configuration

| Variable           | Default   | Description                        |
| ------------------ | --------- | ---------------------------------- |
| `CAPTURE_INTERVAL` | 1000 ms   | Time interval for capturing frames |
| `CAPTURE_WIDTH`    | 320 px    | Width of the video capture         |
| `CAPTURE_HEIGHT`   | 240 px    | Height of the video capture        |
| `BACKEND_URL`      | `/detect` | Flask API URL                      |

---

## 🧪 Testing

1. Start the backend (`localhost:5000`)
2. Start the frontend (`localhost:5173`)
3. Grant camera permissions
4. Click "Start"
5. Test by:

   * Closing your eyes
   * Leaning your head
   * Looking drowsy

---

## 🚯 Alarm Control

* Toggle alarm ON/OFF using the "Alarm" button
* Dismiss warning using the "Dismiss" button
* Alarm auto-stops when alertness is regained

---

## 🧠 Model Note

* The `drowsiness_model.h5` must be trained on eye state or facial expression data.
* Image input size and normalization must match training preprocessing.

---

## 📸 Screenshots

> *(Add screenshots of the working app with warning banner and camera feed)*

---

## 🛡️ Security & Privacy

* No frames are stored or shared.
* All processing happens in real-time on the user's device and private backend.

---

## 🤝 Credits

* UI: Tailwind CSS, ShadCN
* Icons: Lucide React
* ML: TensorFlow
* Backend: Flask + OpenCV

---

## 📄 License

MIT License. Feel free to fork and customize for your own use.
