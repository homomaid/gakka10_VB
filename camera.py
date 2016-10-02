import cv2
import sys
from ball import Ball
# import ball.Ball as Ball


class NormalCamera:
    CV_WAITKEY_ENTER = 13
    CV_WAITKEY_ESC = 27

    def __init__(self, camera_id):
        self.capture = cv2.VideoCapture(camera_id)
        self.capture.set(3, 640)
        self.capture.set(4, 480)

    def detectBallProperty(self, color):
        while True:
            ret, frame = self.capture.read()

            # 色抽出を書くならここ

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gauss = cv2.GaussianBlur(gray, (7, 7), 0)
            result = cv2.HoughCircles(image=gauss, method=cv2.HOUGH_GRADIENT,
                                      dp=1.5, param1=100, param2=110,
                                      minDist=100, minRadius=40, maxRadius=250)

            if result is not None and len(result) > 0:
                circles = result[0]
                for (x, y, r) in circles:
                    print('Radius = ' + str(r))
                    print('len(circles) = ' + str(len(circles)))
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.imshow('Detecting Ball Diameter...', frame)

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ENTER and circles is not None and len(circles) == 1:
                _, _, radius = list(map(int,circles[0]))
                cv2.destroyAllWindows()
                return Ball(radius * 2)
            elif key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()

    def detectBallMotion(self, ball):
        while True:
            ret, frame = self.capture.read()
            cv2.imshow('Detecting Ball Motion...', frame)

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()


class StereoCamera:
    def __init__(self, camera_id):
        print('Write later...')

    def detectBallProperty(self, color):
        print('Write later...')

    def detectBallMotion(self, ball):
        print('Write later...')
