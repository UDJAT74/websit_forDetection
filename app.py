from flask import Flask,render_template,Response,redirect
import cv2 as cv
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import sys,os
import threading
from send_emails import send_emails
from playsound import playsound

# firebase data
import pyrebase
firebaseConfig = {
'apiKey': "AIzaSyB8WFVoksUXJwHSqTFPvDPGeuqyZ4qx86g",
'authDomain': "finding-47a82.firebaseapp.com",
'databaseURL': "https://finding-47a82-default-rtdb.firebaseio.com",
'projectId': "finding-47a82",
'storageBucket': "finding-47a82.appspot.com",
'messagingSenderId': "375040166586",
'appId': "1:375040166586:web:706dfccfae6fa2b7661083",
'measurementId': "G-MG2G02JSPJ"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
database = firebase.database()


model = YOLO("yolov8x.pt")
def detect(frame1):
    global frame
    result = model.predict(frame)
    print(result.length)
    for r in result:
        annotator = Annotator(frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]
            c = box.cls
            annotator.box_label(b, model.names[int(c)], 3)
            # print( int(b[0]),int(c) ) #return class name , c class id
            # x, y, w, h= int(b[0]),int(b[1]),int(b[2]),int(b[3])
            if int(c) == 0:
                cv.imwrite("screenShot.jpg", frame)
                thread = threading.Thread(target=playsound, args=("alarm3.wav",))
                thread.start()
                thread2 = threading.Thread(target=send_emails())
                thread2.start()

            frame = annotator.result()


camera = cv.VideoCapture(0)
app = Flask(__name__)
def generate_frames():
    count = 0
    while True:
        count+=1
        res, frame = camera.read()
        if not res:
            break
        else:
                # thread3=threading.Thread(target=detect(frame))
                # thread3.start()
            result = model.predict(frame)
            for r in result:
                annotator = Annotator(frame)
                boxes=r.boxes
                for box in boxes:
                    b=box.xyxy[0]
                    c=box.cls
                    annotator.box_label(b,model.names[int(c)],3)
                    # print( int(b[0]),int(c) ) #return class name , c class id
                    # x, y, w, h= int(b[0]),int(b[1]),int(b[2]),int(b[3])
                    if int(c)==43:
                        cv.imwrite("screenShot.jpg", frame)
                        thread = threading.Thread(target=playsound, args=("alarm3.wav",))
                        thread.start()
                        # thread2 =threading.Thread(target=send_emails())
                        # thread2.start()

                    # frame=annotator.result()
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def uploadphoto(imgpath):
    count = 1
    if count >= 1:
        count += 1
#       storage.child("tablename").child("detection"+str(count).put(imgpath)


def GenerateFrame():
    camera=cv.VideoCapture(0)
    while True:
        res,frame=camera.read()
        if not res:
            break
        else:
            ret,buffer=cv.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/' )
def login():
    return render_template('index.html')

@app.route('/' , methods=['POST'])
def checklog():
    return redirect("/home")

@app.route("/home")
def homepage():
    return render_template('home.html')
@app.route('/home' , methods=['POST'])
def close():
    camera.release()
    return redirect('/')

@app.route("/detections")
def detections():
    return render_template('detections.html')

@app.route('/video')
def video():
    return Response(GenerateFrame(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)