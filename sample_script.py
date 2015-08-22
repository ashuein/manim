#!/usr/bin/env python

import numpy as np
import itertools as it
from copy import deepcopy
import sys


from animation import *
from mobject import *
from constants import *
from region import *
from scene import Scene, SceneFromVideo
from script_wrapper import command_line_create_scene


class SampleScene(SceneFromVideo):
    def construct(self):
        path = os.path.join(MOVIE_DIR, "EdgeDetectedCountingInBinary35-75.mp4")
        SceneFromVideo.construct(self, path, time_range = (3, 5))
        self.apply_gaussian_blur(sigmaX = 10)
        self.make_all_black_or_white()
        self.name = "BlurEdgeBlurBold"

        # self.animate_over_time_range(
        #     0, 3,
        #     ApplyMethod(Dot().to_edge(LEFT).to_edge, RIGHT)
        # )
       
    def make_all_black_or_white(self):
        self.frames = [
            255*(frame != 0).astype('uint8')
            for frame in self.frames
        ]
        

if __name__ == "__main__":
    command_line_create_scene()