import cv2
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    cv2.imshow('camera capture', frame)

    circles = cv2.HoughCircles(image = gray, method = cv2.HOUGH_GRADIENT, \
                               dp = 1, minDist = 20, minRadius = 20, maxRadius = 200)

    #circles = np.uint16(np.around(circles))

    for i in circles:
        cv2.circle(frame, (i[0], i[1]), i[2], (0,255,0), 2)

    #if circles is not None and len(circles) > 0:
    #    for(x, y, r) in circles:
    #        print(x, y, r)
    #        x, y, r = int(x), int(y), int(r)
    #        cv2.circle(img = frame, center = (x, y), radius = r, color = (255, 0, 0))
    #elif circles is None:
    #    print("if 文が意味をなしていないぞ")

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()



