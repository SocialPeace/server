import os
import cv2
from flask import Flask, render_template, Response
from yolo.utils import yolo
from common.body_parts import BODY_PARTS_BODY_25
from common.body_parts import BODY_PARTS_COCO
from common.body_parts import BODY_PARTS_MPI
from common.pose_pairs import POSE_PAIRS_BODY_25
from common.pose_pairs import POSE_PAIRS_COCO
from common.pose_pairs import POSE_PAIRS_MPI

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = yolo(frame=frame, size=416, score_threshold=0.4, nms_threshold=0.4)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# main page routing
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__' :
    app.run(host='127.0.0.1', port=5050, debug=True)