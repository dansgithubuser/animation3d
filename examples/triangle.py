import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

import animation3d

import math

scene = animation3d.Scene()
for i in range(60):
    scene.set_view(at=(math.sin(math.pi*i/15), 0, -1-i/60))
    scene.add_vertex(-1, -1, -1-i/60,   i/60, 1-i/60,      0)
    scene.add_vertex( 1, -1, -1-i/60,      0,   i/60, 1-i/60)
    scene.add_vertex( 0,  1, -1-i/60, 1-i/60,      0,   i/60)
    scene.frame()
scene.animate()
