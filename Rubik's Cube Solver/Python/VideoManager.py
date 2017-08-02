import numpy as np
import cv2


class VideoManager:

    def __init__(self, source_1, source_2, windowname_1, windowname_2):
        self.camera_1 = cv2.VideoCapture(source_1) if source_1 is not None else None
        self.camera_2 = cv2.VideoCapture(source_2) if source_2 is not None else None
        self.frame_1, self.frame_2 = None, None
        self.ret_1, self.ret_2 = None, None
        self.windowname_1 = windowname_1
        self.windowname_2 = windowname_2

    def set_mouse_callback(self, callback):
        cv2.namedWindow(self.windowname_1)
        cv2.namedWindow(self.windowname_2)
        cv2.setMouseCallback(self.windowname_1, callback, 1)
        cv2.setMouseCallback(self.windowname_2, callback, 2)

    def get_frame(self):
        return (self.ret_1, self.ret_2), (self.frame_1, self.frame_2)

    def update(self):
        if self.camera_1:
            self.ret_1, self.frame_1 = self.camera_1.read()
            self.frame_1 = np.fliplr(self.frame_1).copy()

        if self.camera_2:
            self.ret_2, self.frame_2 = self.camera_2.read()
            self.frame_2 = np.fliplr(self.frame_2).copy()

    def set_frame(self, frame_1, frame_2):
        self.frame_1 = frame_1
        self.frame_2 = frame_2

    def draw(self):
        if self.ret_1:
            cv2.imshow(self.windowname_1, self.frame_1)
        if self.ret_2:
            cv2.imshow(self.windowname_2, self.frame_2)

    def destroy(self):
        if self.camera_1: self.camera_1.release()
        if self.camera_2: self.camera_2.release()
        self.frame_1 = None
        self.frame_2 = None

