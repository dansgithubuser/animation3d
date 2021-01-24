#version 450

uniform mat4 u_proj;
uniform mat4 u_view;

in vec3 a_pos;
in vec3 a_normal;
in vec4 a_color;
in float a_diff;
in float a_spec;
in float a_shin;

out vec3 v_pos;
out vec3 v_normal;
out vec4 v_color;
out float v_diff;
out float v_spec;
out float v_shin;

void main() {
    gl_Position = u_proj * u_view * vec4(a_pos, 1.0);
    v_pos = a_pos.xyz;
    v_normal = a_normal;
    v_color = a_color;
    v_diff = a_diff;
    v_spec = a_spec;
    v_shin = a_shin;
}
