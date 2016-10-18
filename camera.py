import cv2
import sys
import time
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
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

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
            for y in range(0, resolution):
                height = int((y / 32) * len(fgmask))
                ballX_Right = ballX_Left = -1
                for x in range(0, len(fgmask[height])):
                    color = fgmask[height][x]
                    if ballX_Left == -1 and color != 0: # '0' showes black.
                        ballX_Left = x
                    if ballX_Left != -1 and ballX_Right == -1 and color == 0:
                        ballX_Right = x
                if ballX_Right != -1 and ballX_Left != -1 and \
                   ball.radius * 2 * 0.7 <= (ballX_Right - ballX_Left) and \
                   (ballX_Right - ballX_Left) <= ball.radius * 2 * 1.3:
                    if startTime == -1:
                        startTime = time.clock()
                    position = ((ballX_Right + ballX_Left) / 2, height)
                    print('[Debug] position = ' + str(position))
                    positions.append(position)
                    isBallDetected = True
            if isBallDetected is False:
                noneDetectedCount += 1

            if positions != [] and noneDetectedCount >= CAMERA_FPS * waitTime:
                endTime = time.clock()
                t = endTime - startTime - waitTime
                v_x = (positions[-1][0] - positions[0][0]) / t
                if positions[0][1] > len(frame) / 2:
                    print('[Debug] 下から上へのボールの移動を検知しました、x方向の速度の向きを反転します')
                    v_x *= -1
                v_y = abs(positions[-1][1] - positions[0][1]) / t * -1
                velocity = (v_x, v_y)
                return Motion(positions[0][0] - len(frame[0]) / 2, velocity)

            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_R:
                print('[System] R キーが押されました。計測結果をリセットします')
                cv2.destroyAllWindows()
                return -1


class StereoCamera:
    def __init__(self, camera_id):
        print('Write later...')

    def detectBallProperty(self, color):
        print('Write later...')

    def detectBallMotion(self, ball):
        print('Write later...')
