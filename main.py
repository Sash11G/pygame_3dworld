import sys
import math
import pygame
from pygame.locals  import (
    DOUBLEBUF, OPENGL, QUIT,
    MOUSEMOTION, KEYDOWN, MOUSEBUTTONDOWN,
    K_ESCAPE, K_SPACE, K_w, K_s, K_a, K_d
)
from OpenGL.GL      import *
from OpenGL.GLU     import gluPerspective

import settings
from input_handler  import handle_events
from physics        import Physics


# Initialize Pygame and OpenGL context
pygame.init()
pygame.display.set_mode(settings.DISPLAY_SIZE, DOUBLEBUF | OPENGL)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Setup projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(
    settings.FOV,
    settings.DISPLAY_SIZE[0] / settings.DISPLAY_SIZE[1],
    settings.NEAR_PLANE,
    settings.FAR_PLANE
)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Camera state
eye = [0.0, 0.0, 5.0]
yaw, pitch = 0.0, 0.0
first_mouse = True

physics = Physics(eye=eye)

# Jump state
vertical_vel = 0.0
on_ground = True
jump_timer = 0.0

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    # Event handling
    running, yaw, pitch, jump_pressed = handle_events(yaw, pitch)
    if jump_pressed and on_ground:
        vertical_vel = settings.JUMP_SPEED
        on_ground = False


    # Keyboard input for movement
    keys = pygame.key.get_pressed()
    cos_yaw = math.cos(math.radians(yaw))
    sin_yaw = math.sin(math.radians(yaw))
    forward = [sin_yaw, 0, -cos_yaw]
    right_vec = [cos_yaw, 0, sin_yaw]

    def height_at(x, z):
        # pyramid footprint
        if settings.MIN_X <= x <= settings.MAX_X and settings.MIN_Z <= z <= settings.MAX_Z:
            # how “far out” you are, 0 at center → 1 at base edge
            t = max(abs(x), abs(z)) / settings.BASE_HALF
            return settings.GROUND_Y + (h := 2.0) * (1 - t)
        # outside pyramid → flat ground
        return settings.GROUND_Y


    if keys[K_w] or keys[K_s]:
        direction = 1 if keys[K_w] else -1
        dx = forward[0] * settings.MOVE_SPEED * dt * direction
        dz = forward[2] * settings.MOVE_SPEED * dt * direction
        nx, ny, nz = eye[0] + dx, eye[1], eye[2] + dz
        if not (settings.MIN_X < nx < settings.MAX_X and settings.MIN_Z < nz < settings.MAX_Z and settings.OBSTACLE_HEIGHT > ny):
            eye[0], eye[1], eye[2] = nx, ny, nz

    if keys[K_d] or keys[K_a]:
        direction = 1 if keys[K_d] else -1
        dx = right_vec[0] * settings.MOVE_SPEED * dt * direction
        dz = right_vec[2] * settings.MOVE_SPEED * dt * direction
        nx, ny, nz = eye[0] + dx, eye[1], eye[2] + dz
        if not (settings.MIN_X < nx < settings.MAX_X and settings.MIN_Z < nz < settings.MAX_Z and settings.OBSTACLE_HEIGHT > ny):
            eye[0], eye[1], eye[2] = nx, ny, nz

    # Jump cooldown
    jump_timer = max(0.0, jump_timer - dt)
    if keys[K_SPACE] and on_ground and jump_timer == 0.0:
        vertical_vel = settings.JUMP_SPEED
        on_ground = False
        jump_timer = settings.JUMP_INTERVAL

    # Apply gravity
    vertical_vel -= settings.GRAVITY * dt
    eye[1] += vertical_vel * dt

    # # compute surface beneath you
    # floor_y = height_at(eye[0], eye[2]) + settings.CAMERA_HEIGHT

    # if eye[1] <= floor_y:
    #     eye[1]       = floor_y
    #     vertical_vel = 0.0
    #     on_ground    = True
    # else:
    #     on_ground    = False

    # Ground collision
    if -settings.GRID_EXTENT <= eye[0] <= settings.GRID_EXTENT and \
       -settings.GRID_EXTENT <= eye[2] <= settings.GRID_EXTENT:
        if eye[1] <= settings.GROUND_Y + settings.CAMERA_HEIGHT:
            eye[1] = settings.GROUND_Y + settings.CAMERA_HEIGHT
            vertical_vel = 0.0
            on_ground = True
    else:
        on_ground = False

    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Camera transform
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(pitch, 1, 0, 0)
    glRotatef(yaw, 0, 1, 0)
    glTranslatef(-eye[0], -eye[1], -eye[2])

    # Draw grid
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5)
    for i in range(-settings.GRID_EXTENT, settings.GRID_EXTENT + 1):
        glVertex3f(i, settings.GROUND_Y, -settings.GRID_EXTENT)
        glVertex3f(i, settings.GROUND_Y, settings.GRID_EXTENT)
        glVertex3f(-settings.GRID_EXTENT, settings.GROUND_Y, i)
        glVertex3f(settings.GRID_EXTENT, settings.GROUND_Y, i)
    glEnd()

    # Draw pyramid
    h, b = 2.0, settings.BASE_HALF
    apex = (0.0, settings.GROUND_Y + h, 0.0)
    corners = [(-b, settings.GROUND_Y, -b), (b, settings.GROUND_Y, -b),
               (b, settings.GROUND_Y, b), (-b, settings.GROUND_Y, b)]
    glBegin(GL_TRIANGLES)
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]
    for idx in range(4):
        glColor3f(*colors[idx])
        glVertex3fv(apex)
        glVertex3fv(corners[idx])
        glVertex3fv(corners[(idx + 1) % 4])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    for x, y, z in corners:
        glVertex3f(x, y, z)
    glEnd()

    pygame.display.flip()

pygame.quit()
sys.exit()