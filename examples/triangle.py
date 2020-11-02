import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

from animation3d import Color, Material, Point, Scene

import math

scene = Scene()
for i in range(60):
    triangle_z = -2-i/60
    scene.set_view(at=(math.sin(math.pi*i/15), 0, triangle_z))
    scene.add_vertex((-1, -1, triangle_z), Material((  i/60, 1-i/60,      0)))
    scene.add_vertex(( 1, -1, triangle_z), Material((     0,   i/60, 1-i/60)))
    scene.add_vertex(( 0,  1, triangle_z), Material((1-i/60,      0,   i/60)))
    scene.frame()
scene.animate()
