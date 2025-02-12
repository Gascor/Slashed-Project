import json
from objects import Cube, Sphere, Plane, Cylinder, Cone
from utils import load_texture

class MapParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        
        objects = []
        for obj_data in data['objects']:
            obj_type = obj_data['type']
            position = obj_data['position']
            texture_file = obj_data.get('texture')
            color = obj_data.get('color', [1.0, 1.0, 1.0])
            rotation = obj_data.get('rotation', [0, 0, 0])
            scale = obj_data.get('scale', [1, 1, 1])
            size = obj_data.get('size')
            radius = obj_data.get('radius')
            height = obj_data.get('height')
            base = obj_data.get('base')

            if obj_type == 'Cube':
                obj = Cube(position=position)
            elif obj_type == 'Sphere':
                obj = Sphere(position=position)
            elif obj_type == 'Plane':
                obj = Plane(position=position, size=size)
            elif obj_type == 'Cylinder':
                obj = Cylinder(position=position, radius=radius, height=height)
            elif obj_type == 'Cone':
                obj = Cone(position=position, base=base, height=height)
            else:
                continue

            if texture_file:
                texture = load_texture(f"src/textures/{texture_file}")
                obj.texture = texture

            obj.color = color
            obj.rotation = rotation
            obj.scale = scale

            objects.append(obj)
        
        return objects