#version 450

uniform vec3 u_amb;

in vec4 v_color;

out vec4 fragColor;

void main() {
    fragColor = vec4(u_amb * v_color.rgb, v_color.a);
}
