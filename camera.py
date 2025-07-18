import glm
from OpenGL.GL import glRotatef, glTranslatef

class Camera:
    def __init__(self, eye, yaw=0.0, pitch=0.0):
        self.eye   = glm.vec3(eye)
        self.yaw   = yaw
        self.pitch = pitch

    def apply_view(self):
        glRotatef(self.pitch, 1,0,0)
        glRotatef(self.yaw,   0,1,0)
        glTranslatef(-self.eye.x, -self.eye.y, -self.eye.z)

    def rotate(self, dx, dy, sensitivity):
        self.yaw   += dx * sensitivity
        self.pitch -= dy * sensitivity   # invert Y
        self.pitch = max(-89, min(89, self.pitch))
