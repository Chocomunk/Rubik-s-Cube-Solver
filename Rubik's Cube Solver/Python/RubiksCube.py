import numpy as np
from include import kociemba
from defs import *
import Util


class RubiksCube:

    def __init__(self, cube_state=None, solved_state=CubeData.SOLVED_STATE):
        self.cube_state_values = None
        self.cube_state = None
        self.solved_state = solved_state
        if cube_state:
            self.set_state(cube_state)

    def set_state(self, state):
        if isinstance(state, dict):
            self.cube_state_values = state
            self.cube_state = ''
            for facelet in Util.generate_keys()[0]:
                self.cube_state += self.cube_state_values[facelet]
        elif isinstance(state, str):
            self.cube_state = state
            self.cube_state_values = {}
            facelets = Util.generate_keys()[0]
            for i in range(len(facelets)):
                self.cube_state_values[facelets[i]] = self.cube_state[i]

    def get_solution(self):
        # print('UUDDLLRRFFBB')   # Test solution
        # TODO: Use Kociemba's
        return kociemba.solve(self.cube_state)

    def get_state_string(self):
        return self.cube_state
