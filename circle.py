# coding: utf-8

import cv2

capture = cv2.VideoCapture(0)

_, frame = capture.read()
roi = cv2.selectROI('tracker', frame, False, False)

tracker = cv2.Tracker_create("KCF")
tracker.init(frame, roi)

while True:
    ret, frame = capture.read()
    _, position = tracker.update(frame)
    position = list(map(int, position))
    cv2.rectangle(frame, (position[0], position[1]),
                  (position[0] + position[2], position[1] + position[3]),
                  (0, 255, 0))
    cv2.imshow('tracker', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
