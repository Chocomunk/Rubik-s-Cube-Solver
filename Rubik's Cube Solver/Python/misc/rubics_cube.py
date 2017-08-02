import numpy as np
import cv2

cap = cv2.VideoCapture(0)
frame = cv2.imread('mix.jpg')

upper_bounds = []
lower_bounds = []
colors = []

# blue 0
upper_bounds.append(np.array([125,255,255]))
lower_bounds.append(np.array([101,157,101]))
colors.append((255,0,0))

# green 1
upper_bounds.append(np.array([100,255,200]))
lower_bounds.append(np.array([50,110,65]))
colors.append((0,255,0))

# yellow 2
upper_bounds.append(np.array([40,255,255]))
lower_bounds.append(np.array([13,139,76]))
colors.append((0,255,255))

# orange 3
upper_bounds.append(np.array([18,255,228]))
lower_bounds.append(np.array([0,126,19]))
colors.append((0,128,255))

# red 4
upper_bounds.append(np.array([255,255,255]))
lower_bounds.append(np.array([115,120,33]))
colors.append((0,0,255))

# white 5
upper_bounds.append(np.array([105,140,147]))
lower_bounds.append(np.array([74,0,78]))
colors.append((255,255,255))

# black 6
upper_bounds.append(np.array([124,255,100]))
lower_bounds.append(np.array([0,0,0]))
colors.append((0,0,0))

morph_kernel = np.ones((5,5), np.uint8)
bound_index = 6


def parse_keyboard(key):
    # lower bounds
    if key == ord('o'):
        lower_bounds[bound_index][0] += 1
    elif key == ord('l'):
        lower_bounds[bound_index][0] -= 1
    elif key == ord('i'):
        lower_bounds[bound_index][1] += 1
    elif key == ord('k'):
        lower_bounds[bound_index][1] -= 1
    elif key == ord('u'):
        lower_bounds[bound_index][2] += 1
    elif key == ord('j'):
        lower_bounds[bound_index][2] -= 1

    # upper bounds
    elif key == ord('e'):
        upper_bounds[bound_index][0] += 1
    elif key == ord('d'):
        upper_bounds[bound_index][0] -= 1
    elif key == ord('w'):
        upper_bounds[bound_index][1] += 1
    elif key == ord('s'):
        upper_bounds[bound_index][1] -= 1
    elif key == ord('q'):
        upper_bounds[bound_index][2] += 1
    elif key == ord('a'):
        upper_bounds[bound_index][2] -= 1


def draw_contours(inp, outp__img):
    cv2.rectangle(outp__img, (220, 140), (420, 340), (0, 255, 0), 2)

    for i in range(len(upper_bounds)-1):
        m = cv2.inRange(inp[140:340, 220:420], lower_bounds[i], upper_bounds[i])
        m = cv2.erode(m, morph_kernel, iterations=1)
        m = cv2.dilate(m, morph_kernel, iterations=1)
        im2, contours, hierarchy = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # im2, contours, hierarchy = cv2.findContours(m, 1, 2)
        for c in contours:
            # x,y,w,h = cv2.boundingRect(c)
            # cv2.rectangle(outp, (x,y), (x+w,y+h), (0,255,0), 2)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            for j in range(len(box)):
                box[j] = [box[j][0]+220, box[j][1]+140]
            box = np.int0(box)
            cv2.drawContours(outp__img, [box], 0, colors[i], 2)


while True:
    ret, frame = cap.read()
    outp = np.copy(frame)
    outp2 = np.copy(frame)

    filtered = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(filtered, lower_bounds[bound_index], upper_bounds[bound_index])
    # mask = cv2.erode(mask, morph_kernel, iterations=1)
    # mask = cv2.dilate(mask, morph_kernel, iterations=1)
    cv2.bitwise_and(frame, frame, outp2, mask)

    draw_contours(filtered, outp)

    # outp = cv2.cvtColor(outp, cv2.COLOR_HSV2BGR)
    cv2.putText(outp, "Upper: {}".format(upper_bounds[bound_index]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(outp, "Lower: {}".format(lower_bounds[bound_index]), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Rubics', np.hstack((frame, outp, outp2)))
    cv2.imshow('masks', mask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27: # 27 is the escape key
        break
    else:
        parse_keyboard(key)


cap.release()
cv2.destroyAllWindows()