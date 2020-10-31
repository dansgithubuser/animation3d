import moderngl
import numpy as np
from PIL import Image

import os

DIR = os.path.dirname(os.path.realpath(__file__))

class Scene:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.ctx = moderngl.create_context(standalone=True, backend='egl')
        self.fbo = self.ctx.simple_framebuffer((width, height), components=4)
        self.fbo.use()
        with open(os.path.join(DIR, 'vert.glsl')) as f: vert = f.read()
        with open(os.path.join(DIR, 'frag.glsl')) as f: frag = f.read()
        self.prog = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.verts = []

    def add_vertex(self, x, y, r, g, b):
        self.verts.append([x, y, r, g, b])

    def render(self, file_name='frame.png'):
        va = self.ctx.simple_vertex_array(
            self.prog,
            self.ctx.buffer(np.array(self.verts, dtype='f4')),
            'in_vert',
            'in_color',
        )
        va.render(mode=moderngl.TRIANGLES)
        image = Image.frombytes('RGBA', (self.width, self.height), self.fbo.read(components=4))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(file_name)
