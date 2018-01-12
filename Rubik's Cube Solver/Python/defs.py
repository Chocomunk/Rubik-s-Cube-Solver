
class Constants():
    BLUE = (255,0,0); GREEN = (0,255,0); RED = (0,0,255)
    ALL_WINDOWS = -1
    JSON_ENCODER_INDENT_NESTED_LISTS = False


class CubeData():
    SOLVED_STATE = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'


class ColorData():
    # LOWER_BOUND = 'lower_bound'; UPPER_BOUND = 'upper_bound'; COLOR_POINTS = 'color_points'; AVERAGE_COLOR = 'average_color'
    COLOR_MEAN = 'color_mean'; COLOR_STD_DEV = 'color_std_dev'; COLOR_VARIANCE = 'color_variance';
    COLOR_SET_SIZE = 'color_set_size'
    NULL_COLOR = 'Null'; NULL_COLOR_DISTANCE = -1


class DetectionState():
    size = 2
    FACELETS = 0; COLORS = 1


class Facelets():
    U1 = 'U1'; U2 = 'U2'; U3 = 'U3'
    U4 = 'U4'; U5 = 'U5'; U6 = 'U6'
    U7 = 'U7'; U8 = 'U8'; U9 = 'U9'

    D1 = 'D1'; D2 = 'D2'; D3 = 'D3'
    D4 = 'D4'; D5 = 'D5'; D6 = 'D6'
    D7 = 'D7'; D8 = 'D8'; D9 = 'D9'

    L1 = 'L1'; L2 = 'L2'; L3 = 'L3'
    L4 = 'L4'; L5 = 'L5'; L6 = 'L6'
    L7 = 'L7'; L8 = 'L8'; L9 = 'L9'

    R1 = 'R1'; R2 = 'R2'; R3 = 'R3'
    R4 = 'R4'; R5 = 'R5'; R6 = 'R6'
    R7 = 'R7'; R8 = 'R8'; R9 = 'R9'

    F1 = 'F1'; F2 = 'F2'; F3 = 'F3'
    F4 = 'F4'; F5 = 'F5'; F6 = 'F6'
    F7 = 'F7'; F8 = 'F8'; F9 = 'F9'

    B1 = 'B1'; B2 = 'B2'; B3 = 'B3'
    B4 = 'B4'; B5 = 'B5'; B6 = 'B6'
    B7 = 'B7'; B8 = 'B8'; B9 = 'B9'
