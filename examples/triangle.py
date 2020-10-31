import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(DIR, '..'))

import animation3d

scene = animation3d.Scene()
scene.add_vertex(-1.0, -1.0, 1.0, 0.0, 0.0)
scene.add_vertex(+1.0, -1.0, 0.0, 1.0, 0.0)
scene.add_vertex(+0.0, +1.0, 0.0, 0.0, 1.0)
scene.render()
