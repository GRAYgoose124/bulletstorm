#version 330

// Time since burst start
uniform float time;

// (x, y) position passed in
in vec2 in_pos;

// Velocity of particle
in vec2 in_vel;


// Output the color to the fragment shader
out vec4 color;

void main() {
    
    // Color is based on velocity
    color = vec4(in_vel, 0.0, 1.0);

    // Calculate new position
    vec2 new_pos = in_pos + in_vel * time;

    

    // Set the position. (x, y, z, w)
    gl_Position = vec4(new_pos, 0.0, 1);
}