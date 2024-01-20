#version 330

in vec2 velocity;  // The velocity from the vertex shader

out vec4 fragColor;

void main() {
    // Simple coloring based on velocity
    float magnitude = length(velocity);
    vec3 color = vec3(magnitude); // Color the line based on the magnitude of the velocity
    fragColor = vec4(color, 1.0); // Full opacity
}
