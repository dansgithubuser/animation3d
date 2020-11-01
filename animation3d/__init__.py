import moderngl
import numpy as np
from PIL import Image
import pyrr

import glob
import math
import os
import subprocess

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
        self.frame_no = 1
        self.set_perspective()
        self.set_view()

    def set_perspective(self, fovy=90, aspect=None, near=1, far=1000):
        if aspect == None: aspect = self.width / self.height
        perspective = pyrr.matrix44.create_perspective_projection(fovy, aspect, near, far)
        self.prog['u_proj'].write(perspective.astype('f4'))

    def set_view(self, fro=(0, 0, 1), at=(0, 0, 0), up=(0, 1, 0)):
        view = pyrr.matrix44.create_look_at(fro, at, up)
        self.prog['u_view'].write(view.astype('f4'))

    def add_vertex(self, x, y, z, r, g, b):
        self.verts.append([x, y, z, r, g, b])

    def frame(self):
        self.fbo.clear()
        va = self.ctx.simple_vertex_array(
            self.prog,
            self.ctx.buffer(np.array(self.verts, dtype='f4')),
            'in_vert',
            'in_color',
        )
        va.render(mode=moderngl.TRIANGLES)
        image = Image.frombytes('RGBA', (self.width, self.height), self.fbo.read(components=4))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(f'frame-{self.frame_no:06}.png')
        print('completed frame', self.frame_no)
        self.frame_no += 1
        self.verts.clear()

    def animate(self, framerate=30):
        file_name = 'animation.mkv'
        if os.path.exists(file_name): os.remove(file_name)
        subprocess.run(f'ffmpeg -framerate {framerate} -i frame-%06d.png {file_name}'.split())
        for i in glob.glob('frame-*.png'): os.remove(i)
