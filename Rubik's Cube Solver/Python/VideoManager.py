import numpy as np
import cv2
from defs import *


class VideoManager:

    def __init__(self, source_1, source_2, windowname_1, windowname_2):
        self.camera_1 = cv2.VideoCapture(source_1) if source_1 is not None else None
        self.camera_2 = cv2.VideoCapture(source_2) if source_2 is not None else None
        self.frame_1, self.frame_2 = None, None
        self.ret_1, self.ret_2 = False, False
        self.windowname_1 = windowname_1
        self.windowname_2 = windowname_2
        self.pre_processors = []
        self.post_processors = []

    def set_mouse_callback(self, callback):
        cv2.namedWindow(self.windowname_1)
        cv2.namedWindow(self.windowname_2)
        cv2.setMouseCallback(self.windowname_1, callback, 1)
        cv2.setMouseCallback(self.windowname_2, callback, 2)

    def add_pre_processor(self, processor, window_num, *flags):
        self.pre_processors.append((window_num, processor, flags))

    def add_post_processor(self, processor, window_num, *flags):
        self.post_processors.append((window_num, processor, flags))

    def apply_processors(self, processors):
        temp = None
        for window_num, processor, flags in processors:
            if self.ret_1 and (window_num is 1 or window_num is Constants.ALL_WINDOWS):
                if flags and len(flags):
                    temp = processor(self.frame_1, *flags)
                else:
                    temp = processor(self.frame_1)
                self.frame_1 = temp.copy()
            if self.ret_2 and (window_num is 2 or window_num is Constants.ALL_WINDOWS):
                if flags and len(flags):
                    temp = processor(self.frame_2, *flags)
                else:
                    temp = processor(self.frame_2)
                self.frame_2 = temp.copy()

    def get_frame(self):
        return (self.ret_1, self.ret_2), (self.frame_1, self.frame_2)

    def update(self):
        if self.camera_1:
            self.ret_1, self.frame_1 = self.camera_1.read()

        if self.camera_2:
            self.ret_2, self.frame_2 = self.camera_2.read()

        self.apply_processors(self.pre_processors)

    def set_frame(self, frame_1, frame_2):
        self.frame_1 = frame_1
        self.frame_2 = frame_2

    def draw(self):
        self.apply_processors(self.post_processors)
        if self.ret_1:
            cv2.imshow(self.windowname_1, self.frame_1)
        if self.ret_2:
            cv2.imshow(self.windowname_2, self.frame_2)

    def destroy(self):
        if self.camera_1: self.camera_1.release()
        if self.camera_2: self.camera_2.release()
        self.frame_1 = None
        self.frame_2 = None

