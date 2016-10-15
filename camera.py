import cv2
import sys
import time
import pprint
from ball import Ball
from motion import Motion
from constant import CAMERA_WIDTH
from constant import CAMERA_HEIGHT


class NormalCamera:
    CV_WAITKEY_ENTER = 13
    CV_WAITKEY_ESC = 27
    CV_WAITKEY_R = 114

    def __init__(self, camera_id):
        self.capture = cv2.VideoCapture(camera_id)
        self.capture.set(3, CAMERA_WIDTH)
        self.capture.set(4, CAMERA_HEIGHT)

        self.mog = cv2.createBackgroundSubtractorMOG2()

    def detectBallProperty(self):
        while True:
            circles = None
            _, frame = self.capture.read()
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
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_ENTER and circles is not None and len(circles) == 1:
                cv2.destroyAllWindows()
                _, _, radius = list(map(int, circles[0]))
                return Ball(radius)

    def detectBallMotion(self, ball):
        start = -1
        positions = []

        while True:
            _, frame = self.capture.read()
            fgmask = self.mog.apply(frame)
            masked = cv2.bitwise_and(frame, frame, mask=fgmask)
            cv2.imshow('Detecting Ball Motion...', masked)

            isBallDetected = False
            for y in range(0, int(CAMERA_HEIGHT / 32)):
                height = int((y / 32) * CAMERA_HEIGHT)
                ballX_Right = ballX_Left = -1
                for x in range(0, CAMERA_WIDTH):
                    color = fgmask[height][x]
                    if ballX_Left <= -1 and color != 0: # '0' showes black.
                        ballX_Left = x
                    if ballX_Left > -1 and ballX_Right <= -1 and color == 0:
                        ballX_Right = x
                if ballX_Right > -1 and ballX_Left > -1 and (ballX_Right - ballX_Left) >= ball.radius * 2 * 0.8:
                    if start == -1:
                        start = time.clock()
                    position = ((ballX_Right - ballX_Left) / 2, height)
                    print('position = ' + str(position))
                    positions.append(position)
                    isBallDetected = True

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_R:
                print('return -1')
                return -1

            if positions != [] and isBallDetected is False:
                end = time.clock()
                t = end - start
                velocity = (abs(positions[-1][0] - positions[0][0]) / t, abs(positions[-1][1] - positions[0][1]) / t)
                print('time is ' + str(t))
                print('velocity is ' + str(velocity))
                return Motion(positions[0][0], velocity)


class StereoCamera:
    def __init__(self, camera_id):
        print('Write later...')

    def detectBallProperty(self, color):
        print('Write later...')

    def detectBallMotion(self, ball):
        print('Write later...')
