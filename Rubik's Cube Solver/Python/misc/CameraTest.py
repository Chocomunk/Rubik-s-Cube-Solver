import cv2
import numpy as np
import serial

cap_0 = cv2.VideoCapture(0)
cap_1 = cv2.VideoCapture(1)
cap_2 = cv2.VideoCapture(2)
cap_3 = cv2.VideoCapture(3)

# moves = "U2D2L2R2B2F2"
# ser = serial.Serial('COM3', 9600)
# ser.write(moves.encode())


while True:
    r_0, f_0 = cap_0.read()
    r_1, f_1 = cap_1.read()
    r_2, f_2 = cap_2.read()
    r_3, f_3 = cap_3.read()

    if r_0:
        cv2.imshow("Win0", f_0)
    # else:
    #     print("Fix r_0 reeeee")
    if r_1:
        cv2.imshow("Win1", f_1)
    # else:
    #     print("Fix r_1 reeeee")
    if r_2:
        cv2.imshow("Win2", f_2)
    # else:
    #     print("Fix r_2 reeeee")
    if r_3:
        cv2.imshow("Win3", f_3)
    # else:
    #     print("Fix r_3 reeeee")

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
