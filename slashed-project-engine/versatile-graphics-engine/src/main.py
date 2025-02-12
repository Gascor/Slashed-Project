from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time
from engine import Engine
from camera import Camera
from objects import Cube, Sphere, Plane, Cylinder, Cone
from gui import Button, Label
from map import Map
from model import Model
from utils import load_texture
from map_parser import MapParser

screen_width = 2560
screen_height = 1440
last_x, last_y = screen_width // 2, screen_height // 2
first_mouse = True
mouse_in_window = False

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set the camera
    camera.set_view()

    # Render the scene
    engine.render()

    # Render GUI
    button.render()
    label.render()

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def update(value):
    delta_time = 0.016  # Assuming 60 FPS
    engine.update(delta_time)
    glutPostRedisplay()
    glutTimerFunc(int(delta_time * 1000), update, 0)

def keyboard(key, x, y):
    if key == b'w':
        camera.move_forward()
    elif key == b's':
        camera.move_backward()
    elif key == b'a':
        camera.move_left()
    elif key == b'd':
        camera.move_right()

def mouse_motion(x, y):
    global last_x, last_y, first_mouse, mouse_in_window
    center_x, center_y = screen_width // 2, screen_height // 2

    if not mouse_in_window:
        return

    if first_mouse:
        last_x, last_y = center_x, center_y
        first_mouse = False
        glutWarpPointer(center_x, center_y)
        return

    xoffset = x - last_x
    yoffset = last_y - y  # Reversed since y-coordinates go from bottom to top

    last_x, last_y = center_x, center_y
    camera.rotate(xoffset, yoffset)

    # Warp the pointer back to the center of the window
    glutWarpPointer(center_x, center_y)

def mouse_entry(state):
    global mouse_in_window
    if state == GLUT_ENTERED:
        mouse_in_window = True
    elif state == GLUT_LEFT:
        mouse_in_window = False

def main():
    global engine, camera, button, label

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(screen_width, screen_height)
    glutCreateWindow(b"Versatile Graphics Engine")
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [1, 1, 1, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)


    # Initialize the camera with position and look_at arguments
    camera = Camera(position=[0, 0, 5], look_at=[0, 0, 0])
    engine = Engine(camera)

    # Parse the map file
    map_parser = MapParser("src/maps/bunker_map.json")
    objects = map_parser.parse()
    for obj in objects:
        engine.add_object(obj)

    # Create GUI elements
    button = Button(position=[10, 10], size=[100, 50], text="Click Me")
    label = Label(position=[10, 70], text="FPS: 60")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse_motion)
    glutEntryFunc(mouse_entry)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()