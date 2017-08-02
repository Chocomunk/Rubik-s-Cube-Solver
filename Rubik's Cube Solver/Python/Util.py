import json
import cv2
import numpy as np
from defs import *


def draw_points(frames, draw_set):
    for window_num, text_params, circle_params in draw_set:
        if window_num is Constants.ALL_WINDOWS:
            for frame in frames:
                if text_params:
                    cv2.putText(frame, *text_params)
                if circle_params:
                    cv2.circle(frame, *circle_params)
        else:
            if text_params:
                cv2.putText(frames[window_num], *text_params)
            if circle_params:
                cv2.circle(frames[window_num], *circle_params)


def bgr_to_hsv(color):
    _b = color[0]/255
    _g = color[1]/255
    _r = color[2]/255
    c_max = max([_b,_g,_r])
    c_min = min([_b,_g,_r])
    delta = c_max-c_min

    h = 0
    if delta is not 0:
        if c_max is _r: h = 60 * (((_g - _b)/delta) % 6)
        if c_max is _g: h = 60 * (((_b - _r)/delta) + 2)
        if c_max is _b: h = 60 * (((_r - _g)/delta) + 4)
    s = 0 if c_max is 0 else delta/c_max
    v = c_max
    return (h,s,v)


def color_distance(a, b):
    return np.linalg.norm(np.array(a)-np.array(b))


def generate_keys():
    faces = ['U', 'R', 'F', 'D', 'L', 'B']
    facelets = []
    for face in faces:
        for i in range(1,10):
            facelets.append(face+str(i))
    return facelets, faces


def read_file(filename):
    data = []
    with open(filename, 'rt') as f:
        data = json.load(f)
    return data


def write_file(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, sort_keys=True, indent=4, cls=NoListIndentJSONEncoder)


class NoListIndentJSONEncoder(json.JSONEncoder):

    def iterencode(self, o, _one_shot=False):
        list_lvl = 0
        last_was_open_bracket = False
        last_was_close_bracket = False
        last_indent_width = 0
        for s in super(NoListIndentJSONEncoder, self).iterencode(o, _one_shot=_one_shot):
            orig_s = s
            if s.startswith('['):
                list_lvl += 1
                s = s.replace('\n', '').rstrip()
                s = s.replace(' ', '')
                if last_was_open_bracket or last_was_close_bracket:
                    s = '\n' + last_indent_width*' ' + s
                last_was_open_bracket = True
                last_was_close_bracket = False
            else:
                if 0 < list_lvl:
                    s = s.replace('\n', '').rstrip()
                    if s.startswith(','):
                        s = s.replace(' ', '')
                        s = s[0] + ' ' + s[1:]
                    if s and s[-1] == ',':
                        s = s[:-1] + self.item_separator
                    elif s and s[-1] == ':':
                        s = s[:-1] + self.key_separator
                if not s.startswith(',') and s is not '' and s is not None:
                    last_was_open_bracket = False
            if s.endswith(']'):
                list_lvl -= 1
                if last_was_close_bracket:
                    s = '\n' + last_indent_width*' ' + s
                last_was_open_bracket = False
                last_was_close_bracket = True
            elif not s.startswith(',') and s is not '' and s is not None:
                last_was_close_bracket = False

            last_indent_width = len(orig_s) - len(s) - 1

            yield s
