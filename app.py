from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__, template_folder='templates')

# Load YOLOv8 face detection model
try:
    model = YOLO('yolov8n-face.pt')
    print("YOLOv8 model loaded")
except:
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect/', methods=['POST'])
def detect_faces():
    try:
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'No image provided'}), 400
        
        file = request.files['image']
        img = Image.open(file.stream)
        img_array = np.array(img)
        
        if model is None:
            return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
        
        # Detect faces with YOLOv8
        results = model(img_array)
        recognized_people = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                
                recognized_people.append({
                    'name': 'Face',
                    'confidence': round(1 - conf, 3),
                    'box': [int(x1), int(y1), int(x2), int(y2)],
                    'is_allowed': True
                })
        
        return jsonify({
            'status': 'success',
            'people_count': len(recognized_people),
            'recognized_people': recognized_people
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
