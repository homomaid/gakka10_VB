import numpy as np
import cv2
import os

cascade_path = "/usr/local/opt/opencv3/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
cascade      = cv2.CascadeClassifier(cascade_path)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

color = (255, 127, 191)

while True:
    ret, frame = cap.read()
    facerect = cascade.detectMultiScale(frame, scaleFactor = 1.2, \
                                        minNeighbors = 2, minSize = (10, 10))
    for rect in facerect:
        cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness = 2)
    cv2.imshow('camera capture', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

