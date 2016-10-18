import sys
from motion import Motion
from constant import MODE_3D
from constant import FILE_PATH
from constant import LANE_WIDTH
from constant import CAMERA_WIDTH
from camera import StereoCamera
from camera import NormalCamera

def calcBallMotionForUnity(motion):
    position  = motion.position / CAMERA_WIDTH * LANE_WIDTH
    velocityX = motion.velocity[0] / CAMERA_WIDTH * LANE_WIDTH
    velocityY = motion.velocity[1] / CAMERA_WIDTH * LANE_WIDTH

    return Motion(position, (velocityX, velocityY))

print('[System] カメラ ID を入力してください')
sys.stdout.write('（よくわからない場合 0 と入れてください）: ')
camera_id = int(input())

cam = StereoCamera(camera_id) if MODE_3D is True else NormalCamera(camera_id)
print('[System] ボールを画面上に入れて、半径を取得してください')
ball = cam.detectBallProperty()
print('[System] 計測モードに入ります。ボールを投げてください。')
while True:
    motion = cam.detectBallMotion(ball)
    if motion == -1:
        continue

    motionForUnity = calcBallMotionForUnity(motion)
    print('[System] 計測完了！')
    print('[System] 初期位置: ' + str(motionForUnity.position))
    print('[System] 速度: ' + str(motionForUnity.velocity))

    file = open(FILE_PATH, 'w+')
    file.write(str(motionForUnity.position) + "\n" +
               str(motionForUnity.velocity[0]) + '\n' +
               str(motionForUnity.velocity[1]))
    print('[System] vector.txtに計測結果を記録しました。')
