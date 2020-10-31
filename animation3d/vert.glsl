#version 450

uniform mat4 u_proj;

in vec3 in_vert;
in vec3 in_color;

out vec3 color;

void main() {
    gl_Position = u_proj * vec4(in_vert, 1.0);
    color = in_color;
}
