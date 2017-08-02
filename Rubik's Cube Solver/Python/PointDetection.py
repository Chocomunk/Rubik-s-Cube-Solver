import numpy as np
import cv2
import Util
import copy
from defs import *


class PointDetection:

    def __init__(self, videomanager, points_file=None, colors_file=None):
        self.videomanager = videomanager
        self.points_file = points_file
        self.colors_file = colors_file

        self.facelets, self.faces = Util.generate_keys()
        self.points = Util.read_file(self.points_file)
        self.colors = Util.read_file(self.colors_file)
        self.colors_temp = None
        self.colors_state = dict.fromkeys(self.facelets)

        self.detection_state = DetectionState.FACELETS
        self.curr_facelet_index = 0
        self.curr_face_index = 0

        if not len(self.points):
            self.clear_data()   # Detection state is already FACELETS
        if not len(self.colors):
            self.detection_state = DetectionState.COLORS
            self.clear_data()
            self.detection_state = DetectionState.FACELETS

        self.isCompleteCube = False

        self.videomanager.set_mouse_callback(self.on_mouse)

    def get_color(self, point_value):
        matching_colors = []
        for color, data in self.colors.items():
            if data[ColorData.POINTS] is not None and len(data[ColorData.POINTS]) > 0:
                matches_curr_color = True
                for i in range(len(point_value)):
                    matches_curr_color = (matches_curr_color and
                                          data[ColorData.LOWER_BOUND][i] <= point_value[i] <= data[ColorData.UPPER_BOUND][i])
                if matches_curr_color:
                    matching_colors.append((color, Util.color_distance(point_value, data[ColorData.AVERAGE_COLOR])))

        if not matching_colors:
            matching_colors.append((ColorData.NULL_COLOR, ColorData.NULL_COLOR_DISTANCE))

        return [e[0] for e in sorted(matching_colors, key=lambda matching_color: matching_color[1])]

    def cycle_state_variable(self, step):
        if self.detection_state is DetectionState.FACELETS:
            self.curr_facelet_index = (self.curr_facelet_index + step) % len(self.facelets)
        if self.detection_state is DetectionState.COLORS:
            self.curr_face_index = (self.curr_face_index + step) % len(self.faces)

    def cycle_detection_state(self):
        self.detection_state = (self.detection_state + 1) % DetectionState.size
        if self.detection_state is DetectionState.COLORS:
            self.colors_temp = copy.deepcopy(self.colors)
        if self.detection_state is DetectionState.FACELETS:
            self.colors = self.colors_temp
            del self.colors_temp

    def update(self):
        ret, frames = self.videomanager.get_frame()

        draw_set = None
        if self.detection_state is DetectionState.FACELETS:
            draw_set = self.apply_facelet_points(ret, frames)
        if self.detection_state is DetectionState.COLORS:
            draw_set = self.apply_color_points(ret, frames)

        if draw_set:
            Util.draw_points(frames, draw_set)

        self.videomanager.set_frame(frames[0], frames[1])

    def apply_facelet_points(self, ret, frames):
        draw_set = []
        all_points_set = True
        self.isCompleteCube = True
        for facelet, point in self.points.items():
            if not point:
                all_points_set = False
                self.isCompleteCube = False
                continue
            text_color = Constants.BLUE if facelet == self.facelets[self.curr_facelet_index] else Constants.GREEN
            x, y, window_num = int(point[0]), int(point[1]), point[2]-1
            if ret[window_num]:
                value = self.get_color(frames[window_num][y,x])
                if ColorData.NULL_COLOR in value: self.isCompleteCube = False
                self.colors_state[facelet] = value

                draw_set.append((window_num,
                                 (" {}: {}".format(facelet, value), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, text_color),
                                 ((x, y), 1, text_color, 3)
                                 ))

        draw_set.append((Constants.ALL_WINDOWS,
                        (self.facelets[self.curr_facelet_index], (580, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                            Constants.BLUE if all_points_set
                            else Constants.GREEN if self.points[self.facelets[self.curr_facelet_index]]
                            else Constants.RED),
                         None
                         ))
        return draw_set

    def apply_color_points(self, ret, frames):
        lower_bound = self.colors[self.faces[self.curr_face_index]][ColorData.LOWER_BOUND]
        upper_bound = self.colors[self.faces[self.curr_face_index]][ColorData.UPPER_BOUND]
        points = self.colors[self.faces[self.curr_face_index]][ColorData.POINTS]

        average_color = None
        draw_set = []
        if points:
            average_color = np.array([0,0,0])
            for p in points:
                x, y, window_num = int(p[0]), int(p[1]), p[2]-1
                if ret[window_num]:
                    value = frames[window_num][y,x]

                    if lower_bound is None: lower_bound = [int(e) for e in value]
                    if upper_bound is None: upper_bound = [int(e) for e in value]

                    for i in range(len(value)):
                        if value[i] < lower_bound[i]:
                            lower_bound[i] = int(value[i])
                        if value[i] > upper_bound[i]:
                            upper_bound[i] = int(value[i])
                        average_color[i] += value[i]

                    draw_set.append((window_num,
                                     (" {}".format(value), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, Constants.GREEN),
                                     ((x, y), 1, Constants.BLUE, 3)
                                     ))

            average_color /= len(points)
            self.colors[self.faces[self.curr_face_index]][ColorData.AVERAGE_COLOR] = [e.item() for e in average_color]
            self.colors[self.faces[self.curr_face_index]][ColorData.LOWER_BOUND] = lower_bound
            self.colors[self.faces[self.curr_face_index]][ColorData.UPPER_BOUND] = upper_bound

        if average_color is None:
            average_color = list(Constants.RED)

        draw_set.append((Constants.ALL_WINDOWS,
                         ("{}: {} {}".format(self.faces[self.curr_face_index], lower_bound, upper_bound),
                          (40,40), cv2.FONT_HERSHEY_SIMPLEX, .5, average_color),
                         ((25,35), 3, average_color, 5)
                         ))
        return draw_set

    def on_mouse(self, event, x, y, flags, window_num):
        if self.detection_state is DetectionState.FACELETS:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.points[self.facelets[self.curr_facelet_index]] = (x,y,window_num)
            if event == cv2.EVENT_RBUTTONDOWN:
                self.points[self.facelets[self.curr_facelet_index]] = None
            self.write_data()

        if self.detection_state is DetectionState.COLORS:
            if event == cv2.EVENT_LBUTTONDOWN:
                if not self.colors[self.faces[self.curr_face_index]][ColorData.POINTS]:
                    self.colors[self.faces[self.curr_face_index]][ColorData.POINTS] = []
                self.colors[self.faces[self.curr_face_index]][ColorData.POINTS].append((x,y,window_num))
            if event == cv2.EVENT_RBUTTONDOWN:
                self.colors[self.faces[self.curr_face_index]][ColorData.LOWER_BOUND] = None
                self.colors[self.faces[self.curr_face_index]][ColorData.UPPER_BOUND] = None
                self.colors[self.faces[self.curr_face_index]][ColorData.POINTS] = []

    def clear_data(self):
        if self.detection_state is DetectionState.FACELETS:
            self.points = dict.fromkeys(self.facelets)
            Util.write_file(self.points_file, self.points)
        if self.detection_state is DetectionState.COLORS:
            for key in self.faces:
                self.colors[key] = {}
                self.colors[key][ColorData.LOWER_BOUND] = None
                self.colors[key][ColorData.UPPER_BOUND] = None
                self.colors[key][ColorData.AVERAGE_COLOR] = None
                self.colors[key][ColorData.POINTS] = []
            Util.write_file(self.colors_file, self.colors)

    def write_data(self):
        if self.detection_state is DetectionState.FACELETS:
            Util.write_file(self.points_file, self.points)
        if self.detection_state is DetectionState.COLORS:
            del self.colors_temp[self.faces[self.curr_face_index]]
            self.colors_temp[self.faces[self.curr_face_index]] = copy.deepcopy(self.colors[self.faces[self.curr_face_index]])
            Util.write_file(self.colors_file, self.colors_temp)
