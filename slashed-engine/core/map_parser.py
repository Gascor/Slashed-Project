import json
from core.scene import Cube, Plane

class MapParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        
        objects = []
        for obj_data in data["objects"]:
            obj_type = obj_data["type"]
            position = obj_data["position"]
            rotation = obj_data["rotation"]
            scale = obj_data["scale"]
            texture = obj_data.get("texture", None)

            if obj_type == "Cube":
                obj = Cube()
            elif obj_type == "Plane":
                obj = Plane(texture)
            else:
                continue

            obj.position = position
            obj.rotation = rotation
            obj.scale = scale
            objects.append(obj)
        
        return objects