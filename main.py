import constant
import camera
import ball

print('please input camera id : ')
camera_id = input()

camera = StereoCamera.new(camera_id) if MODE_3D is True else NormalCamera.new(camera_id)
ball = camera.detectBallProperty(BALL_COLOR)

while True:
    camera.detectBallMotion(ball)
