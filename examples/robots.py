import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

from animation3d import Color, Material, Point, Scene

import math

scene = Scene()
scene.set_ambient_light(Color())
for i in range(120):
    t = i / 30
    w = math.pi * t / 8
    # view
    view_distance = 3
    scene.set_view(
        fro=Point(t + view_distance * math.sin(w), 2, view_distance * math.cos(w)),
        at=Point(t, 1),
    )
    # floor
    scene.add_plane(Point(), Point(y=1), Material(diffuse=1))
    # lights
    street_size = 3
    light_space = 8
    light_horizon = 64
    x_light = math.floor(scene.view.fro.x / light_space) * light_space
    for x in range(x_light - light_horizon, x_light + light_horizon, light_space):
        z = street_size * [-1, 1][x // light_space % 2]
        scene.add_light(Point(x, 8, z), Color(w=30, r=30, g=20))
    #
    scene.frame()
scene.animate()
