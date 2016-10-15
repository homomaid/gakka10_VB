import sys
from constant import MODE_3D
from constant import FILE_PATH
from camera import StereoCamera
from camera import NormalCamera

sys.stdout.write('please input camera id : ')
camera_id = int(input())

cam = StereoCamera(camera_id) if MODE_3D is True else NormalCamera(camera_id)
ball = cam.detectBallProperty()
while True:
    motion = cam.detectBallMotion(ball)
    if motion == -1:
        continue
