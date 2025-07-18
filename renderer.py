from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

def render_scene(camera, settings):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera.apply_view()
    # draw your world
    from world import draw_grid, draw_pyramid
    draw_grid(settings)
    draw_pyramid(settings)
