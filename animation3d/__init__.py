import moderngl
import numpy as np
from PIL import Image
import pyrr

import glob
import math
import os
import subprocess

DIR = os.path.dirname(os.path.realpath(__file__))

def Point(x=0, y=0, z=0):
    return (x, y, z)

def Color(r=0, g=0, b=0, a=1.0, w=0):
    return (r+w, g+w, b+w, a)

class Material:
    def __init__(
        self,
        color=Color(w=0.5),
        diffuse=1,
        specular=1,
        shininess=100,
    ):
        if len(color) == 3: color = color + (1,)
        self.color = color
        self.diff = diffuse
        self.spec = specular
        self.shin = shininess

class Scene:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.ctx = moderngl.create_context(standalone=True, backend='egl')
        self.texture = self.ctx.texture((width, height), components=4)
        self.fb = self.ctx.framebuffer(
            self.texture,
            self.ctx.depth_renderbuffer((width, height)),
        )
        with open(os.path.join(DIR, 'main.vert.glsl')) as f: vert = f.read()
        with open(os.path.join(DIR, 'main.frag.glsl')) as f: frag = f.read()
        self.prog = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.verts = []
        self.lights = []
        self.frame_no = 1
        self.set_perspective()
        self.set_view()
        self.set_ambient_light(Color(w=1))
        self.acc = Accumulator(self.ctx, width, height)

    def set_ambient_light(self, color):
        prev = self.prog['u_amb'].value
        self.prog['u_amb'] = color[0:3]
        return prev

    def set_perspective(self, fov=90, aspect=None, near=1, far=1000):
        if aspect == None: aspect = self.width / self.height
        fovy = fov / aspect
        perspective = pyrr.matrix44.create_perspective_projection(fovy, aspect, near, far)
        self.prog['u_proj'].write(perspective.astype('f4'))

    def set_view(self, fro=Point(z=1), at=Point(), up=Point(y=1)):
        view = pyrr.matrix44.create_look_at(fro, at, up)
        self.prog['u_view'].write(view.astype('f4'))

    def add_vertex(self, at, normal=Point(), material=Material()):
        self.verts.append([
            *at,
            *normal,
            *material.color,
            material.diff,
            material.spec,
            material.shin,
        ])

    def add_light(self, at, color=Color(w=1)):
        self.lights.append((at, color[0:3]))

    def frame(self):
        va = self.ctx.vertex_array(
            self.prog,
            [(
                self.ctx.buffer(np.array(self.verts, dtype='f4')),
                '3f 3f 4f 1f 1f 1f',
                'a_pos',
                'a_normal',
                'a_color',
                'a_diff',
                'a_spec',
                'a_shin',
            )],
        )
        amb = None
        self.acc.clear()
        for light in self.lights:
            self.fb.use()
            self.fb.clear()
            self.prog['u_light_pos'] = light[0]
            self.prog['u_light_color'] = light[1]
            va.render(mode=moderngl.TRIANGLES)
            self.acc.add(self.texture)
            if not amb: amb = self.set_ambient_light(Color())
        self.set_ambient_light(amb)
        image = Image.frombytes('RGBA', (self.width, self.height), self.acc.read())
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(f'frame-{self.frame_no:06}.png')
        print('completed frame', self.frame_no)
        self.frame_no += 1
        self.verts.clear()
        self.lights.clear()

    def animate(self, frame_rate=30):
        file_name = 'animation.mkv'
        if os.path.exists(file_name): os.remove(file_name)
        subprocess.run(f'ffmpeg -framerate {frame_rate} -i frame-%06d.png {file_name}'.split())
        for i in glob.glob('frame-*.png'): os.remove(i)

class Accumulator:
    def __init__(self, ctx, width, height):
        self.width = width
        self.height = height
        self.ctx = ctx
        self.texture = self.ctx.texture((width, height), components=4)
        self.fb = self.ctx.framebuffer(self.texture)
        with open(os.path.join(DIR, 'acc.vert.glsl')) as f: vert = f.read()
        with open(os.path.join(DIR, 'acc.frag.glsl')) as f: frag = f.read()
        self.prog = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.prog['u_a'] = 0
        self.prog['u_b'] = 1
        self.texture.use()

    def clear(self):
        self.fb.clear()

    def add(self, texture):
        texture.use(1)
        self.fb.use()
        verts = [
            [-1, -1],
            [-1, +1],
            [+1, +1],
            [+1, -1],
        ]
        va = self.ctx.vertex_array(
            self.prog,
            [(
                self.ctx.buffer(np.array(verts, dtype='f4')),
                '2f',
                'a_pos',
            )],
        )
        va.render(mode=moderngl.TRIANGLE_FAN)

    def read(self):
        return self.fb.read(components=4)
