# coding: utf-8

import cv2

capture = cv2.VideoCapture(2)
capture.set(3, 640)
capture.set(4, 480)

while True:
    ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    preprocessed = cv2.GaussianBlur(gray, (7, 7), 0)

    result = cv2.HoughCircles(image=preprocessed, method=cv2.HOUGH_GRADIENT,
                              dp=1.5, param1=100, param2=110,
                              minDist=100, minRadius=40, maxRadius=250)

    if result is not None and len(result) > 0:
        circles = result[0]
        for(x, y, r) in circles:
            print(x, y, r)
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

    cv2.imshow('ball', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
