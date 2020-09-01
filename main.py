#!/usr/bin/env python3

import os
import signal
import sys

import pygame
import autopy

# check if environment
current_status = os.environ.get("CONTROLLER_TO_MOUSE_ENABLED", "False")
# Toggle status
if current_status == "True":
    os.environ["CONTROLLER_TO_MOUSE_ENABLED"] = "False"
    pid = os.environ["CONTROLLER_TO_MOUSE_PID"]
    os.kill(pid, signal.SIGKILL)
    sys.exit()

if current_status == "False":
    os.environ["CONTROLLER_TO_MOUSE_ENABLED"] = "True"
    os.environ["CONTROLLER_TO_MOUSE_PID"] = str(os.getpid())


pygame.init()

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
number_of_axis = joystick.get_numaxes()
number_of_buttons = joystick.get_numbuttons()


clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(2):
                autopy.mouse.click()

    left_axis_state = joystick.get_axis(0), joystick.get_axis(1)
    right_axis_state = joystick.get_axis(2), joystick.get_axis(3)

    button_state_array = [joystick.get_button(i) for i in range(number_of_buttons)]
    current_mouse_x, current_mouse_y = autopy.mouse.location()

    delta_x_mouse_location = left_axis_state[0] * 5
    delta_y_mouse_location = left_axis_state[1] * 5

    new_mouse_x = current_mouse_x + delta_x_mouse_location
    new_mouse_y = current_mouse_y + delta_y_mouse_location
    if autopy.screen.is_point_visible(new_mouse_x, new_mouse_y):
        print(new_mouse_x, new_mouse_y)
        autopy.mouse.move(new_mouse_x, new_mouse_y)

    clock.tick(120)

pygame.joystick.quit()
pygame.quit()