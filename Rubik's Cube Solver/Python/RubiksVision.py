import numpy as np
import cv2
import traceback
from RubiksCube import *
from PointDetection import *
from VideoManager import *

videoman = VideoManager(source_1=1, source_2=None, windowname_1="Cam 1", windowname_2="Cam 2")
pointdet = PointDetection(videomanager=videoman, points_file="data/points.json", colors_file="data/colors.json")
cube = RubiksCube()


def parse_keyboard(key_stroke):
    if key_stroke == ord('w'):
        pointdet.write_data()
    if key_stroke == ord('e'):
        pointdet.clear_data()
    if key_stroke == ord('a'):
        pointdet.cycle_state_variable(-1)
    if key_stroke == ord('s'):
        pointdet.cycle_state_variable(1)
    if key_stroke == ord('z'):
        pointdet.cycle_detection_state()
    if key_stroke == ord('\r'):
        if pointdet.isCompleteCube:
            cube.set_state(pointdet.colors_state)
            print(cube.get_state_string())
        else:
            print("REEEEE: NOT A COMPLETE CUBE!!!")


while True:
    try:
        videoman.update()
        pointdet.update()
        videoman.draw()

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            videoman.destroy()
            break
        else:
            parse_keyboard(key)
    except Exception as e:
        videoman.destroy()
        traceback.print_exc()
        break
