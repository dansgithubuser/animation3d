#version 450

uniform mat4 u_proj;
uniform mat4 u_view;

in vec3 in_vert;
in vec3 in_color;

out vec3 color;

void main() {
    gl_Position = u_proj * u_view * vec4(in_vert, 1.0);
    color = in_color;
}
