import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

from animation3d import Color, Material, Point, Scene

import math

scene = Scene()
scene.set_ambient_light(Color())
for i in range(30):
    t = i / 30
    w = math.pi * t / 8
    # view
    view_distance = 3
    scene.set_view(
        fro=Point(t + view_distance * math.sin(w), 2, view_distance * math.cos(w)),
        at=Point(t, 1),
    )
    # floor
    scene.add_plane(Point(), Point(y=1), Material(specular=0))
    # lights
    street_size = 3
    light_space = 4
    light_horizon = 8
    x_light = math.floor(scene.view.fro.x / light_space) * light_space
    for x in range(x_light - light_horizon, x_light + light_horizon, light_space):
        z = street_size * [-1, 1][x // light_space % 2]
        scene.add_light(Point(x, 8, z), Color(w=0.3, r=0.3, g=0.2))
    #
    scene.frame()
scene.animate()
