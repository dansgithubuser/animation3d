#version 450

uniform sampler2D u_a;
uniform sampler2D u_b;

in vec2 v_pos;

out vec4 fragColor;

void main() {
    const vec2 pos = v_pos / 2.0 + 0.5;
    fragColor = texture(u_a, pos) + texture(u_b, pos);
}
