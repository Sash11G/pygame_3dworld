from OpenGL.GL import glBegin, glEnd, glColor3f, glVertex3f, GL_LINES, GL_TRIANGLES, GL_QUADS

def draw_grid(settings):
    glBegin(GL_LINES)
    glColor3f(0.5,0.5,0.5)
    for i in range(-settings.GRID_EXTENT, settings.GRID_EXTENT+1):
        glVertex3f( i, settings.GROUND_Y, -settings.GRID_EXTENT)
        glVertex3f( i, settings.GROUND_Y,  settings.GRID_EXTENT)
        glVertex3f(-settings.GRID_EXTENT, settings.GROUND_Y, i)
        glVertex3f( settings.GRID_EXTENT, settings.GROUND_Y, i)
    glEnd()

def draw_pyramid(settings):
    h, b = 2.0, settings.BASE_HALF
    apex    = (0, settings.GROUND_Y + h, 0)
    corners = [
        (-b, settings.GROUND_Y, -b),
        ( b, settings.GROUND_Y, -b),
        ( b, settings.GROUND_Y,  b),
        (-b, settings.GROUND_Y,  b),
    ]
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0)]

    glBegin(GL_TRIANGLES)
    for i in range(4):
        glColor3f(*colors[i])
        glVertex3f(*apex)
        glVertex3f(*corners[i])
        glVertex3f(*corners[(i+1)%4])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.5,0.5,0.5)
    for x,y,z in corners:
        glVertex3f(x,y,z)
    glEnd()
