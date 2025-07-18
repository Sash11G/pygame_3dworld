# physics.py
import math
import settings
from pygame.locals  import (
    K_w, K_s, K_a, K_d
)
class Physics:
    def __init__(self, eye, yaw=0.0, pitch=0.0):
        self.eye = list(eye)
        self.yaw = yaw
        self.pitch = pitch
        self.vertical_vel = 0.0
        self.on_ground = True
        self.jump_timer = 0.0

    def update(self, dt, keys, jump_pressed):
        # 1) handle jump input
        if jump_pressed and self.on_ground:
            self.vertical_vel = settings.JUMP_SPEED
            self.on_ground = False

        # 2) apply gravity
        self.vertical_vel -= settings.GRAVITY * dt
        self.eye[1] += self.vertical_vel * dt

        # 3) ground collision
        if abs(self.eye[0]) <= settings.GRID_EXTENT and abs(self.eye[2]) <= settings.GRID_EXTENT:
            if self.eye[1] <= settings.GROUND_Y + settings.CAMERA_HEIGHT:
                self.eye[1] = settings.GROUND_Y + settings.CAMERA_HEIGHT
                self.vertical_vel = 0.0
                self.on_ground = True
        else:
            self.on_ground = False

        # 4) movement
        cos_yaw = math.cos(math.radians(self.yaw))
        sin_yaw = math.sin(math.radians(self.yaw))
        forward = ( sin_yaw, 0, -cos_yaw )
        right_vec = ( cos_yaw, 0,  sin_yaw )

        if keys[K_w] or keys[K_s]:
            d = 1 if keys[K_w] else -1
            dx, dz = forward[0]*d, forward[2]*d
            self._try_move(dx, dz, dt)
        if keys[K_d] or keys[K_a]:
            d = 1 if keys[K_d] else -1
            dx, dz = right_vec[0]*d, right_vec[2]*d
            self._try_move(dx, dz, dt)

        # 5) countdown jump timer
        self.jump_timer = max(0.0, self.jump_timer - dt)

    def _try_move(self, dx, dz, dt):
        nx = self.eye[0] + dx * settings.MOVE_SPEED * dt
        nz = self.eye[2] + dz * settings.MOVE_SPEED * dt
        if settings.MIN_X < nx < settings.MAX_X and settings.MIN_Z < nz < settings.MAX_Z:
            self.eye[0], self.eye[2] = nx, nz
