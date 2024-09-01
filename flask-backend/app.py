from flask import Flask, Response, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load the DNN model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

def gen_frames():
    camera = cv2.VideoCapture(0)  # Capture video from the webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Prepare the image for DNN processing
            h, w = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                         (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()

            # Count the number of faces
            num_faces = 0

            # Process detections
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:  # Confidence threshold
                    num_faces += 1
                    box = detections[0, 0, i, 3:7] * [w, h, w, h]
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            
            socketio.emit('face_detected', {'message': f'{num_faces} face(s) detected!'})

            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/count_faces', methods=['GET'])
def count_faces():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    if not success:
        return jsonify({'error': 'Could not read frame'}), 500
    
    # Prepare the image for DNN processing
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    # Count the number of faces
    num_faces = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            num_faces += 1
    
    return jsonify({'num_faces': num_faces})

if __name__ == '__main__':
    socketio.run(app, debug=True)
