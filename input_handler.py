# input_handler.py

import pygame
from pygame.locals import (
    QUIT, MOUSEMOTION, KEYDOWN, MOUSEBUTTONDOWN,
    K_ESCAPE, K_SPACE
)
import settings


def handle_events(yaw, pitch):
    """
    Process user input events.
    Returns:
        running (bool): whether the main loop should continue
        yaw (float), pitch (float): updated camera angles
        jump_pressed (bool): whether jump was triggered
    """
    running = True
    jump_pressed = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            dx, dy = pygame.mouse.get_rel()
            yaw += dx * settings.MOUSE_SENSITIVITY
            pitch += dy * settings.MOUSE_SENSITIVITY
            pitch = max(-89.0, min(89.0, pitch))
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        elif event.type == KEYDOWN and event.key == K_SPACE:
            jump_pressed = True

    return running, yaw, pitch, jump_pressed