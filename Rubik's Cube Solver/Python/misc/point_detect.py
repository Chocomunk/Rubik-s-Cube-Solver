import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
outp = np.copy(frame)

points = []

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))

cv2.namedWindow("Window")
cv2.setMouseCallback("Window", onMouse)

while True:
    ret, frame = cap.read()
    frame = np.fliplr(frame)
    outp = np.copy(frame)

    for p in points:
        value = outp[p[1], p[0]]
        cv2.putText(outp, "({}, {}): {}".format(p[0],p[1],value), (p[0],p[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0))
        cv2.circle(outp, (p[0], p[1]), 1, (255,0,0), 3)

    cv2.imshow("Window", outp)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break