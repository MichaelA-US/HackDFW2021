import cv2
import os

def farEnough(width):
    return True if width <= 50 else False

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video = cv2.VideoCapture(0)

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

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()