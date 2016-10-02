import sys
from constant import MODE_3D
from constant import BALL_COLOR
from camera import StereoCamera
from camera import NormalCamera

sys.stdout.write('please input camera id : ')
camera_id = int(input())

cam = StereoCamera(camera_id) if MODE_3D is True else NormalCamera(camera_id)
ball = cam.detectBallProperty(BALL_COLOR)

while True:
    motion = cam.detectBallMotion(ball)
    print("Send Unity's application the data of motion capture")
