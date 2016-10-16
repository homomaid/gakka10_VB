import cv2
import sys
import time
import pprint
from ball import Ball
from motion import Motion
from constant import CAMERA_FPS
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
                    print('[System] 円の半径: ' + str(int(r)))
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.imshow('Detecting Ball Property...', frame)

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_ENTER and \
                 circles is not None and len(circles) == 1:
                cv2.destroyAllWindows()
                _, _, radius = list(map(int, circles[0]))
                return Ball(int(radius))

    def detectBallMotion(self, ball, waitTime = 0.5, resolution = 32):
        startTime = -1
        positions = []
        noneDetectedCount = 0

        while True:
            _, frame = self.capture.read()
            fgmask = self.mog.apply(frame)
            masked = cv2.bitwise_and(frame, frame, mask=fgmask)
            cv2.imshow('Detecting Ball Motion...', masked)

            isBallDetected = False
            for y in range(0, int(CAMERA_HEIGHT / resolution)):
                height = int((y / 32) * CAMERA_HEIGHT)
                ballX_Right = ballX_Left = -1
                for x in range(0, CAMERA_WIDTH):
                    color = fgmask[height][x]
                    if ballX_Left <= -1 and color != 0: # '0' showes black.
                        ballX_Left = x
                    if ballX_Left > -1 and ballX_Right <= -1 and color == 0:
                        ballX_Right = x
                if ballX_Right > -1 and ballX_Left > -1 and \
                   ball.radius * 2 * 0.8 <= (ballX_Right - ballX_Left) and \
                   (ballX_Right - ballX_Left) <= ball.radius * 2 * 1.2:
                    if startTime == -1:
                        startTime = time.clock()
                    position = ((ballX_Right - ballX_Left) / 2, height)
                    print('[Debug] position = ' + str(position))
                    positions.append(position)
                    isBallDetected = True

            if isBallDetected is False:
                noneDetectedCount += 1

            if positions != [] and noneDetectedCount >= CAMERA_FPS * waitTime:
                endTime = time.clock()
                t = endTime - startTime
                velocity = (abs(positions[-1][0] - positions[0][0]) / t, \
                            abs(positions[-1][1] - positions[0][1]) / t)
                return Motion(positions[0][0], velocity)

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_R:
                print('[System] R キーが押されました。計測結果をリセットします')
                return -1


class StereoCamera:
    def __init__(self, camera_id):
        print('Write later...')

    def detectBallProperty(self, color):
        print('Write later...')

    def detectBallMotion(self, ball):
        print('Write later...')
