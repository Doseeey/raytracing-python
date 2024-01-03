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

struct Plane {
    vec3 center;
    vec3 tangent;
    vec3 bitangent;
    vec3 normal;
    float uMin;
    float uMax;
    float vMin;
    float vMax;
    vec3 color;
};

struct RenderState {
    float t;
    vec3 color;
    bool hit;
    vec3 position; //where ray hit
    vec3 normal;
};

// input/output
layout(local_size_x = 8, local_size_y = 8) in;
layout(rgba32f, binding = 0) uniform image2D img_output;

//Scene Data
uniform Camera viewer;
layout(rgba32f, binding = 1) readonly uniform image2D objects;
uniform samplerCube sky_cube;
uniform float sphereCount;
uniform float planeCount;

RenderState trace(Ray ray);

RenderState hit(Ray ray, Sphere sphere, float tMin, float tMax, RenderState renderState); 

RenderState hit(Ray ray, Plane plane, float tMin, float tMax, RenderState renderState); 

Sphere unpackSphere(int index);

Plane unpackPlane(int index);

void main() {
    ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 screen_size = imageSize(img_output);
    float horizontalCoefficient = ((float(pixel_coords.x) * 2 - screen_size.x) / screen_size.x);
    float verticalCoefficient = ((float(pixel_coords.y) * 2 - screen_size.y) / screen_size.x);

    //Init ray - wychodzi z kamery w kierunku osi x
    Ray ray;
    ray.origin = viewer.position;
    ray.direction = viewer.forwards + horizontalCoefficient * viewer.right +  verticalCoefficient * viewer.up; 

    // Find color of pixel, where ray is shooting
    vec3 pixel = vec3(1.0);
    vec3 finalColor = vec3(0.0);
    
    RenderState renderState;
    for (int i = 0; i < 4; i++) {
        renderState = trace(ray);

        pixel = pixel * renderState.color;

        if (!renderState.hit) {
            break;
        }

        ray.origin = renderState.position;
        ray.direction = reflect(ray.direction, renderState.normal);
    }

    finalColor = pixel;

    imageStore(img_output, pixel_coords, vec4(finalColor, 1.0));
}

RenderState trace(Ray ray) {
    //Returns sphere color if ray hit the sphere

    float nearestHit = 99999999;
    RenderState renderState;
    renderState.color = vec3(texture(sky_cube, ray.direction));
    renderState.hit = false;

    for (int i = 0; i < sphereCount; i++) {
        RenderState newRenderState = hit(ray, unpackSphere(i), 0.001, nearestHit, renderState);

        if (newRenderState.hit) {
            nearestHit = newRenderState.t;
            renderState = newRenderState;
        }
    }

    for (int i = int(sphereCount); i < sphereCount + planeCount; i++) {
        RenderState newRenderState = hit(ray, unpackPlane(i), 0.001, nearestHit, renderState);

        if (newRenderState.hit) {
            nearestHit = newRenderState.t;
            renderState = newRenderState;
        }
    }

    return renderState;
}

RenderState hit(Ray ray, Sphere sphere, float tMin, float tMax, RenderState renderState) {
    vec3 co = ray.origin - sphere.center;

    float a = dot(ray.direction, ray.direction);
    float b = 2 * dot(ray.direction, co);
    float c = dot(co, co) - sphere.radius * sphere.radius;

    float delta = b * b - (4 * a * c);

    if (delta > 0) {
        float t = (-b - sqrt(delta)) / (2 * a); //-sqrt(delta) bedzie blizsze viewera, dlatego tylko to jest istotne

        if (t > tMin && t < tMax) {

            renderState.position = ray.origin + t * ray.direction;
            renderState.normal = normalize(renderState.position - sphere.center);
            renderState.t = t;
            renderState.color = sphere.color;
            renderState.hit = true;
            return renderState;
        }
    }

    renderState.hit = false;
    return renderState;
}

RenderState hit(Ray ray, Plane plane, float tMin, float tMax, RenderState renderState) {
    //wyznacznik musi byc rozny od 0 
    //ujemny wyznacznik := plaszczyzna widoczna od wewnatrz
    //dodatni wyznacznik := plaszczyzna widoczna od zewnatrz
    
    float denominator = dot(plane.normal, ray.direction);

    if (denominator != 0) {
        float t = dot(plane.center - ray.origin, plane.normal) / denominator;

        if (t > tMin && t < tMax) {
            vec3 testPoint = ray.origin + t * ray.direction;
            vec3 testDirection = testPoint - plane.center;

            float u = dot(testDirection, plane.tangent);
            float v = dot(testDirection, plane.bitangent);

            if (u > plane.uMin && u < plane.uMax && v > plane.vMin && v < plane.vMax) {
                renderState.position = testPoint;
                renderState.normal = plane.normal;
                renderState.t = t;
                renderState.color = plane.color;
                renderState.hit = true;
                return renderState;
            }
        }
    }

    renderState.hit = false;
    return renderState;
}


Sphere unpackSphere(int index) {
    //sphere := (x, y, z, radius) (r, g, b, _) (_, _, _, _) (_, _, _, _) (_, _, _, _)
    Sphere sphere;

    vec4 attributeChunk = imageLoad(objects, ivec2(0, index));
    sphere.center = attributeChunk.xyz;
    sphere.radius = attributeChunk.w;

    attributeChunk = imageLoad(objects, ivec2(1, index));
    sphere.color = attributeChunk.xyz;

    return sphere;
}

Plane unpackPlane(int index) {
    //plane  := (x, y, z, tx) (ty, tz, bx, by) (bz, nx, ny, nz) (umin, umax, vmin, vmax) (r, g, b, _)
    Plane plane;

    vec4 attributeChunk = imageLoad(objects, ivec2(0, index));
    plane.center = attributeChunk.xyz;
    plane.tangent.x = attributeChunk.w;

    attributeChunk = imageLoad(objects, ivec2(1, index));
    plane.tangent.yz = attributeChunk.xy;
    plane.bitangent.xy = attributeChunk.zw;

    attributeChunk = imageLoad(objects, ivec2(2, index));
    plane.bitangent.z = attributeChunk.x;
    plane.normal = attributeChunk.yzw;

    attributeChunk = imageLoad(objects, ivec2(3, index));
    plane.uMin = attributeChunk.x;
    plane.uMax = attributeChunk.y;
    plane.vMin = attributeChunk.z;
    plane.vMax = attributeChunk.w;

    attributeChunk = imageLoad(objects, ivec2(4, index));
    plane.color = attributeChunk.xyz;

    return plane;
}