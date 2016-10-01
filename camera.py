import cv2


class NormalCamera:
    def __init__(self, camera_id):
        self.capture = cv2.VideoCapture(camera_id)

    def detectBallProperty(self, color):
        print('あとでかけ')

    def detectBallMotion(self, ball):
        print('あとでかけ')


class StereoCamera:
    def __init__(self, camera_id):
        print('あとでかけ')

    def detectBallProperty(self, color):
        print('あとでかけ')

    def detectBallMotion(self, ball):
        print('あとでかけ')
