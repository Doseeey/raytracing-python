#version 430

struct Sphere {
    vec3 center;
    float radius;
    vec3 color;
};

struct Camera {
    vec3 position;
    vec3 forwards;
    vec3 right;
    vec3 up;
};

struct Ray {
    vec3 origin;
    vec3 direction;
};

// input/output
layout(local_size_x = 1, local_size_y = 1) in;
layout(rgba32f, binding = 0) uniform image2D img_output;

void main() {
    ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 screen_size = imageSize(img_output);
    float horizontalCoefficient = ((float(pixel_coords.x) * 2 - screen_size.x) / screen_size.x);
    float verticalCoefficient = ((float(pixel_coords.y) * 2 - screen_size.y) / screen_size.x);

    // Black plane
    vec3 pixel = vec3(0.0, 0.0, 0.0);

    //Pozycja kamery w centrum układu
    Camera camera;
    camera.position = vec3(0.0);
    camera.forwards = vec3(1.0, 0.0, 0.0);
    camera.right = vec3(0.0, 1.0, 0.0);
    camera.up = vec3(0.0, 0.0, 1.0);

    //Sfera polozona na osi X w odleglosci center, o promieniu radius
    Sphere sphere;
    sphere.center = vec3(10.0, 5.0, 5.0);
    sphere.radius = 1.0;
    sphere.color = vec3(1.0, 1.0, 0);

    //Init ray - wychodzi z kamery w kierunku osi x
    Ray ray;
    ray.origin = camera.position;
    ray.direction = camera.forwards + horizontalCoefficient * camera.right +  verticalCoefficient * camera.up; 

    //Test uderzenia sfery - rozwiazanie rownania kwadratowego dla t
    float a = dot(ray.direction, ray.direction);
    float b = 2.0 * dot(ray.direction, ray.origin - sphere.center);
    float c = dot(ray.origin - sphere.center, ray.origin - sphere.center) - sphere.radius * sphere.radius;

    float delta = b * b - 4.0 * a * c;

    if (delta > 0) {
        pixel += sphere.color;
    }

    imageStore(img_output, pixel_coords, vec4(pixel, 1.0));
}