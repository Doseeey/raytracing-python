#version 430 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec2 vertexTextureCoordinate;

out vec2 fragmentTextureCoordinate;

void main() {
    gl_Position = vec4(vertexPos, 1.0);
    fragmentTextureCoordinate = vertexTextureCoordinate;
}