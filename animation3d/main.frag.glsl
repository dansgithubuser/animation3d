#version 450

uniform mat4 u_view;
uniform vec3 u_amb;
uniform vec3 u_light_pos;
uniform vec3 u_light_color;

in vec3 v_pos;
in vec3 v_normal;
in vec4 v_color;
in float v_diff;
in float v_spec;
in float v_shin;

out vec4 fragColor;

void main() {
    const vec3 light_pos = (u_view * vec4(u_light_pos, 1.0)).xyz;
    const vec3 light_dir = normalize(light_pos - v_pos);
    const vec3 reflect_dir = reflect(-light_dir, v_normal);
    const vec3 eye_dir = -normalize(v_pos);
    const vec3 diff = v_diff * u_light_color * max(0.0, dot(v_normal, light_dir));
    const vec3 spec = v_spec * u_light_color * pow(max(0.0, dot(eye_dir, reflect_dir)), v_shin);
    fragColor = vec4((u_amb + diff + spec) * v_color.rgb, v_color.a);
}
