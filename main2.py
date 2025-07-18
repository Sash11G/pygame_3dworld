import sys, os
import math
import pygame
from pygame.locals import (
    DOUBLEBUF, OPENGL, QUIT,
    MOUSEMOTION, KEYDOWN, MOUSEBUTTONDOWN, K_ESCAPE, K_SPACE,
    K_w, K_s, K_a, K_d
)
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

# Settings
os.environ['SDL_VIDEO_WINDOW_POS'] = "1920,0"
display_size = (1200, 675)
fov = 60
near, far = 0.1, 1000.0
move_speed = 5.0       # units per second
mouse_sensitivity = 0.2  # degrees per pixel

GRID_EXTENT = 20   # how far the grid extends in X/Z
GROUND_Y    = -1   # Y‑level of the grid
BASE_HALF = 1.0
MIN_X, MAX_X = -BASE_HALF, BASE_HALF
MIN_Z, MAX_Z = -BASE_HALF, BASE_HALF

# Jumping logic
camera_height = 1.0  
jump_speed     = 5.0
gravity        = 9.8
vertical_vel  = 0.0
on_ground      = True
jump_interval  = 0.5    # seconds between jumps
jump_timer     = 0.0
camera_height  = 1.0    # eye’s y‑offset above GROUND_Y

# Initialize Pygame and OpenGL context
pygame.init()
pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Setup projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(fov, display_size[0] / display_size[1], near, far)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Camera state
eye = [0.0, 0.0, 5.0]   # camera position
yaw, pitch = 0.0, 0.0    # rotation angles
last_mouse = (display_size[0] // 2, display_size[1] // 2)
first_mouse = True

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0  # delta time (s)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            dx, dy = pygame.mouse.get_rel()
            if first_mouse:
                first_mouse = False
            yaw += dx * mouse_sensitivity
            pitch += dy * mouse_sensitivity
            pitch = max(-89.0, min(89.0, pitch))
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            # enable OS cursor and window dragging
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # hide cursor and lock it back to window
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        # Jumping event handling
        elif event.type == KEYDOWN and event.key == K_SPACE:
            if on_ground:
                vertical_velocity = jump_speed
                on_ground = False

    
    # Keyboard input for movement
    keys = pygame.key.get_pressed()
    cos_yaw = math.cos(math.radians(yaw))
    sin_yaw = math.sin(math.radians(yaw))
    forward = [sin_yaw, 0, -cos_yaw]
    right_vec = [cos_yaw, 0, sin_yaw]
    # forward/backward
    if keys[K_w] or keys[K_s]:
        direction = 1 if keys[K_w] else -1
        dx = forward[0] * move_speed * dt * direction
        dz = forward[2] * move_speed * dt * direction
        nx, nz = eye[0] + dx, eye[2] + dz
        # only commit if outside the pyramid footprint:
        if not (MIN_X < nx < MAX_X and MIN_Z < nz < MAX_Z):
            eye[0], eye[2] = nx, nz

    # right/left
    if keys[K_d] or keys[K_a]:
        direction = 1 if keys[K_d] else -1
        dx = right_vec[0] * move_speed * dt * direction
        dz = right_vec[2] * move_speed * dt * direction
        nx, nz = eye[0] + dx, eye[2] + dz
        if not (MIN_X < nx < MAX_X and MIN_Z < nz < MAX_Z):
            eye[0], eye[2] = nx, nz

    # decrement the jump cooldown
    jump_timer = max(0.0, jump_timer - dt)
    # auto‑jump while SPACE is held
    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and on_ground and jump_timer == 0.0:
        vertical_vel = jump_speed
        on_ground    = False
        jump_timer   = jump_interval
    # subtract gravity
    vertical_vel -= gravity * dt
    # move camera up/down
    eye[1] += vertical_vel * dt
    # ground collision
    # only collide with ground if inside the grid square:
    if -GRID_EXTENT <= eye[0] <= GRID_EXTENT and -GRID_EXTENT <= eye[2] <= GRID_EXTENT:
        if eye[1] <= GROUND_Y + camera_height:
            eye[1] = GROUND_Y + camera_height
            vertical_vel = 0.0
            on_ground = True
    else:
        # outside the grid: no ground -> keep falling
        on_ground = False
    """
    if keys[K_w]:  # forward
        eye[0] += forward[0] * move_speed * dt
        eye[2] += forward[2] * move_speed * dt
    if keys[K_s]:  # backward
        eye[0] -= forward[0] * move_speed * dt
        eye[2] -= forward[2] * move_speed * dt
    if keys[K_d]:  # right
        eye[0] += right_vec[0] * move_speed * dt
        eye[2] += right_vec[2] * move_speed * dt
    if keys[K_a]:  # left
        eye[0] -= right_vec[0] * move_speed * dt
        eye[2] -= right_vec[2] * move_speed * dt
    """
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Camera transform
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(pitch, 1, 0, 0)
    glRotatef(yaw,   0, 1, 0)
    glTranslatef(-eye[0], -eye[1], -eye[2])

    # Draw a larger floor grid at y = GROUND_Y
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5)
    for i in range(-GRID_EXTENT, GRID_EXTENT+1):
        glVertex3f( i, GROUND_Y, -GRID_EXTENT)
        glVertex3f( i, GROUND_Y,  GRID_EXTENT)
        glVertex3f(-GRID_EXTENT, GROUND_Y,  i)
        glVertex3f( GRID_EXTENT, GROUND_Y,  i)
    glEnd()

    # Draw pyramid resting on the grid
    h, b = 2.0, 1.0  # height and base half-size
    apex    = (0.0, GROUND_Y + h, 0.0)
    corners = [(-b, GROUND_Y, -b), ( b, GROUND_Y, -b),
               ( b, GROUND_Y,  b), (-b, GROUND_Y,  b)]
    # sides
    glBegin(GL_TRIANGLES)
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0)]
    for idx in range(4):
        glColor3f(*colors[idx])
        glVertex3fv(apex)
        glVertex3fv(corners[idx])
        glVertex3fv(corners[(idx+1) % 4])
    glEnd()
    # base
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    for x, y, z in corners:
        glVertex3f(x, y, z)
    glEnd()
    # Swap buffers
    pygame.display.flip()

pygame.quit()
sys.exit()