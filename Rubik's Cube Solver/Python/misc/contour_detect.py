import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# frame = cv2.imread('mix.jpg')

while True:
    ret, frame = cap.read()

    filtered = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(filtered, (0,0,0), (124,255,100))

    gray = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 75, L2gradient=True)

    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    for c in contours:
        # rect = cv2.minAreaRect(c)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        hull = cv2.convexHull(c)
        # cv2.drawContours(frame, [hull], 0, (255,0,0), 2)

        area = cv2.contourArea(hull)
        perim = cv2.arcLength(hull,True)
        if area > 800 and perim > 80 and area < 2600:
            ratio = area/((perim/4)**2)
            if ratio>0.9 and ratio<1.2:
                cv2.drawContours(frame, [c], 0, (0,0,255), 2)

    outp = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    cv2.imshow('Rubik\'s', np.hstack((frame,outp)))
    cv2.imshow('Contours', edges)
    cv2.imshow('Mask', mask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break