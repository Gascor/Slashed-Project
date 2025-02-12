import math

class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def add(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, factor):
        return Vector3D(self.x * factor, self.y * factor, self.z * factor)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D()
        return self.scale(1 / mag)

class Camera:
    def __init__(self, position, look_at):
        self.position = position
        self.look_at = look_at
        self.up = Vector3D(0, 1, 0)

    def get_view_matrix(self):
        forward = self.look_at.subtract(self.position).normalize()
        right = self.up.cross(forward).normalize()
        up = forward.cross(right)
        return [right, up, forward]

class Engine3D:
    def __init__(self, camera):
        self.camera = camera
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        view_matrix = self.camera.get_view_matrix()
        for obj in self.objects:
            print(f"Rendering object at: {obj.position}")

class Object3D:
    def __init__(self, position):
        self.position = position

# Example setup
camera = Camera(Vector3D(0, 0, -5), Vector3D(0, 0, 0))
engine = Engine3D(camera)

cube = Object3D(Vector3D(1, 1, 1))
engine.add_object(cube)
engine.render()