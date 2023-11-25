#version 430 core

in vec2 fragmentTextureCoordinate;

uniform sampler2D framebuffer;

out vec4 finalColor;

void main() {
    finalColor = texture(framebuffer, fragmentTextureCoordinate);
}