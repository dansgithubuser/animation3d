import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

from animation3d import Color, Material, Point, Scene

import math

scene = Scene()
scene.set_ambient_light(Color(w=0.2))
for i in range(60):
    triangle_z = -2-i/60
    scene.set_view(at=Point(math.sin(math.pi*i/15), 0, triangle_z))
    scene.add_vertex(Point(-1, -1, triangle_z), Point(z=1), Material(Color(r=1)))
    scene.add_vertex(Point( 1, -1, triangle_z), Point(z=1), Material(Color(g=1)))
    scene.add_vertex(Point( 0,  1, triangle_z), Point(z=1), Material(Color(b=1)))
    scene.add_light(Point(y=4*math.sin(math.pi*i/15), z=5), Color(w=0.2, r=0.4))
    scene.add_light(Point(x=4*math.sin(math.pi*i/15), z=5), Color(w=0.2, b=0.4))
    scene.frame()
scene.animate()
