#version 450

uniform mat4 u_proj;
uniform mat4 u_view;

in vec3 a_pos;
in vec4 a_color;

out vec4 v_color;

void main() {
    gl_Position = u_proj * u_view * vec4(a_pos, 1.0);
    v_color = a_color;
}
