import cv2

video = cv2.VideoCapture(0)

while True:
    frame = video.read()

    cv2.imshow('Video', frame)