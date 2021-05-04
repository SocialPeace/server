import os
import cv2
from models import db,User
from flask import Flask, render_template, Response
from yolo.utils import yolo
from common.body_parts import BODY_PARTS_BODY_25
from common.body_parts import BODY_PARTS_COCO
from common.body_parts import BODY_PARTS_MPI
from common.pose_pairs import POSE_PAIRS_BODY_25
from common.pose_pairs import POSE_PAIRS_COCO
from common.pose_pairs import POSE_PAIRS_MPI
from oauth2client.contrib.flask_util import UserOAuth2





basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app = Flask(__name__)   
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'
app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '130638438522-6ssernn61r7n6mec3r4b3h811ca4lj58.apps.googleusercontent.com'
app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = '3UAxrK1V1PNuvIQgaudC4bin'
oauth2 = UserOAuth2(app)
# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


db.init_app(app)
db.app = app
db.create_all()


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
@app.route("/main")
@oauth2.required
def login(): 
    # query = db.session.query(User.email == oauth2.email ).all()
     
    # if len(query) == 0 :
    #     db = User(email=oauth2.email,name=oauth2.user_id)
    #     db.add(user)
    #     db.commit()


    print( "Hello, {} ({})".format(oauth2.email, oauth2.user_id))
    return render_template('main.html')
 
    #return render_template('index.html')

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/location")
def main():
    return render_template('location.html')

 
@app.route("/mypage")
def mypage():
    return render_template('mypage.html')

@app.route("/location_reg")
@oauth2.required
def location_reg(req):
    # user = session.query(Model).filter(Model.name == 'lowell').update({'addr': ,'lat':,'lng':});
    session.commit()
    return render_template('mypage.html')

if __name__ == '__main__' :
    app.run(host='127.0.0.1', port=5050, debug=True) 