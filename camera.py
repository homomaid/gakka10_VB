import cv2
import sys
import time
from ball import Ball
from motion import Motion
from constant import CAMERA_WIDTH
from constant import CAMERA_HEIGHT


class NormalCamera:
    CV_WAITKEY_ENTER = 13
    CV_WAITKEY_ESC = 27
    CV_WAITKEY_R = 115

    def extractColor(self, src, h_th_low, h_th_high, s_th, v_th):
        hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)

        if h_th_low > h_th_high:
            _, h_dst_low = cv2.threshold(h, h_th_low,  255, cv2.THRESH_BINARY)
            _, h_dst_high = cv2.threshold(h, h_th_high, 255, cv2.THRESH_BINARY_INV)
            h_dst = cv2.bitwise_or(h_dst_low, h_dst_high)
        else:
            _, h_dst = cv2.threshold(h, h_th_low, 255, cv2.THRESH_TOZERO)
            _, h_dst = cv2.threshold(h_dst, h_th_high, 255, cv2.THRESH_TOZERO_INV)
            _, h_dst = cv2.threshold(h_dst, 0, 255, cv2.THRESH_BINARY)

        _, s_dst = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
        _, v_dst = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)

        return cv2.bitwise_and(cv2.bitwise_and(h_dst, s_dst), v_dst)

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
                x, y, radius = list(map(int, circles[0]))
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                return Ball(radius, hsv[y][x])

    def detectBallMotion(self, ball):
        positions = []
        while True:
            _, frame = self.capture.read()
            extracted = self.extractColor(frame, ball.color[0]-20,
                                          ball.color[0]+20, ball.color[1],
                                          ball.color[2])
            masked = cv2.bitwise_and(frame, frame, mask=extracted)

            isBallDetected = False
            for y in range(0, int(CAMERA_HEIGHT / 32)):
                height = int((y / 32) * CAMERA_HEIGHT)
                ballX_Right = ballX_Left = -1
                start = end = -1

                for x in range(0, CAMERA_WIDTH):
                    color = masked[height][x]
                    if ballX_Right == -1 and color != 255:  # white
                        ballX_Right = x
                    if ballX_Right != -1 and ballX_Left == -1 and color == 255:
                        ballX_Left = x
                    if ballX_Right != -1 and ballX_Left == -1 and (ballX_Left - ballX_Right) >= ball.radius * 2 * 0.9:
                        if start == -1:
                            start = time.time()
                        position = ((ballX_Left - ballX_Right) / 2, height)
                    positions.append(position)
                    isBallDetected = True

            cv2.imshow('Detecting Ball Motion...', masked)
            key = cv2.waitKey(1)
            if key == self.CV_WAITKEY_ESC:
                self.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
            elif key == self.CV_WAITKEY_R:
                return -1
            if positions != [] and isBallDetected is False:
                end = time.time()
                t = end - start
                velocity = (int((abs(positions[-1][0] - positions[0][0])/t)),
                            int((abs(positions[-1][1] - positions[-1][0])/t)))
                print(position[0][0])
                print(velocity)
                return Motion(positions[0][0], velocity)


class StereoCamera:
    def __init__(self, camera_id):
        print('Write later...')

    def detectBallProperty(self, color):
        print('Write later...')

    def detectBallMotion(self, ball):
        print('Write later...')
