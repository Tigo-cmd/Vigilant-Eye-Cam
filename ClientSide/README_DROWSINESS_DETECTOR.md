# Vigilant Eye Cam - Drowsiness Detection System

A comprehensive React-based drowsiness detection system that uses real-time webcam analysis to detect driver fatigue and prevent accidents.

## 🚀 Features

- **Real-time Video Capture**: Uses modern `getUserMedia` API for webcam access
- **Drowsiness Detection**: Sends frames to backend every 1 second for AI analysis
- **Visual & Audio Alerts**: Warning banner and customizable alarm sound
- **Responsive Design**: Mobile-friendly layout with proper aspect ratios
- **Error Handling**: Graceful handling of camera permissions and network failures
- **Retry Logic**: Automatic retry mechanism for network requests
- **Accessibility**: ARIA labels, keyboard navigation, and high contrast design

## 🛠 Technology Stack

- **Framework**: Vite + React 18 + TypeScript
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: shadcn/ui components
- **Audio**: Web Audio API for alarm generation
- **Camera**: MediaDevices API for webcam access

## 📋 Prerequisites

### Frontend (This Project)
- Node.js 16+ and npm
- Modern web browser with camera support
- HTTPS connection (required for camera access in production)

### Backend Requirements
You need a backend service running at `http://localhost:5000/detect` that:

1. **Accepts POST requests** with `Content-Type: image/jpeg`
2. **Returns JSON response** in format:
   ```json
   {
     "drowsy": boolean,
     "confidence": number // 0.0 to 1.0
   }
   ```
3. **Has CORS enabled** for frontend requests

#### Backend Setup Example (Python Flask)
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/detect', methods=['POST'])
def detect_drowsiness():
    try:
        # Get image data
        image_data = request.get_data()
        
        # Convert to OpenCV format
        image = Image.open(io.BytesIO(image_data))
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Your drowsiness detection logic here
        # This is a placeholder - implement your actual ML model
        drowsy = False  # Replace with actual detection
        confidence = 0.85  # Replace with actual confidence score
        
        return jsonify({
            'drowsy': drowsy,
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Development Setup
```bash
# Start the development server
npm run dev
```

The application will be available at `http://localhost:8080`

### 3. Production Build
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file if you need to customize the backend URL:

```env
VITE_BACKEND_URL=http://localhost:5000/detect
```

### CORS Configuration
If you're getting CORS errors, you have three options:

1. **Enable CORS on your backend** (recommended)
2. **Use Vite proxy** - Add to `vite.config.ts`:
   ```typescript
   export default defineConfig({
     server: {
       proxy: {
         '/api': {
           target: 'http://localhost:5000',
           changeOrigin: true,
           rewrite: (path) => path.replace(/^\/api/, '')
         }
       }
     }
   })
   ```
3. **Run Chrome with disabled security** (development only):
   ```bash
   chrome --disable-web-security --user-data-dir=/tmp/chrome_dev
   ```

## 🎯 Usage

### Basic Integration
```tsx
import React from 'react';
import DrowsinessDetector from '@/components/DrowsinessDetector';

function App() {
  return (
    <div className="min-h-screen bg-background">
      <DrowsinessDetector />
    </div>
  );
}

export default App;
```

### Component Features

1. **Camera Initialization**
   - Automatically requests camera permissions on mount
   - Handles permission denial with user-friendly error messages
   - Provides retry functionality

2. **Detection Process**
   - Captures frames at 320x240 resolution every 1 second
   - Converts frames to JPEG with 80% quality
   - Sends to backend with retry logic (max 2 retries)

3. **Alert System**
   - Visual warning banner appears when drowsiness detected
   - Audio alarm plays (can be toggled on/off)
   - Warning clears after 2 consecutive alert frames

4. **User Controls**
   - Start/Stop detection
   - Reset system
   - Toggle alarm on/off
   - Manual warning dismissal

## 🎨 Customization

### Styling
The component uses a custom design system defined in:
- `src/index.css` - CSS custom properties
- `tailwind.config.ts` - Tailwind extensions

Key design tokens:
- `--primary`: Main brand color (blue)
- `--warning`: Warning color (amber)
- `--danger`: Danger color (red)
- `--success`: Success color (green)

### Configuration Constants
Modify these constants in `DrowsinessDetector.tsx`:

```typescript
const BACKEND_URL = 'http://localhost:5000/detect'; // Backend endpoint
const CAPTURE_INTERVAL = 1000; // Capture frequency (ms)
const CAPTURE_WIDTH = 320; // Frame width
const CAPTURE_HEIGHT = 240; // Frame height
const MAX_RETRIES = 2; // Network retry attempts
const RETRY_DELAY = 1000; // Retry delay (ms)
```

## 📱 Mobile Considerations

- **Camera Access**: Requires HTTPS in production
- **Performance**: Optimized frame capture for mobile devices
- **Layout**: Responsive design that works on all screen sizes
- **Battery**: Efficient processing to minimize battery drain

## 🐛 Troubleshooting

### Common Issues

1. **Camera Permission Denied**
   - Solution: Use HTTPS in production, check browser settings

2. **CORS Errors**
   - Solution: Enable CORS on backend or use proxy configuration

3. **Backend Connection Failed**
   - Solution: Ensure backend is running on correct port, check firewall

4. **Poor Detection Accuracy**
   - Solution: Improve lighting, ensure face is visible, fine-tune backend model

### Debug Mode
Enable detailed logging by opening browser dev tools. All errors are prefixed with `[DrowsinessDetector]`.

## 🔐 Security Considerations

- **Camera Access**: Only request permissions when needed
- **Data Privacy**: Frames are sent to backend but not stored locally
- **HTTPS**: Required for camera access in production
- **Input Validation**: Backend should validate image data

## 📊 Performance Optimization

- **Frame Resolution**: 320x240 for optimal bandwidth usage
- **Compression**: JPEG at 80% quality
- **Request Throttling**: 1-second intervals prevent backend overload
- **Memory Management**: Proper cleanup of video streams and timers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Lovable platform. See license terms in the main project.

## 🆘 Support

For issues related to:
- **Frontend**: Check browser console for errors
- **Backend**: Verify endpoint response format
- **Camera**: Ensure proper permissions and HTTPS
- **Performance**: Monitor network tab in dev tools

Remember: This is a safety-critical application. Test thoroughly before deployment in real-world scenarios.