import cv2
import os
from flask import Flask, render_template,Response

video = cv2.VideoCapture(0)
app = Flask(__name__, template_folder="../Website")

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def farEnough(width):
    return True if width <= 50 else False

def gen():
    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        largest = (-1, -1, -1, -1)
        for (x, y, w, h) in faces:
            largest = (x, y, w, h) if w > largest[2] else largest
 
        if largest[0] != -1:
            isFarEnough = farEnough(w)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0) if isFarEnough else (0, 0, 255), 2)

            if not isFarEnough:
                cv2.putText(frame, 'Move farther away', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Face not detected', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        #cv2.imshow('Video', frame)
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

@app.route("/")
def index():
    return render_template('eyeexam.html')

@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)