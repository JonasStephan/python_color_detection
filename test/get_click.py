# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:58:19 2025

@author: jonas.stephan
"""

from pynput.mouse import Listener

# This function will be called when the mouse is clicked
def on_click(x, y, button, pressed):
    if pressed:
        print("Button = ", button)
        print(type(button))
        print(f"Mouse clicked at ({x}, {y}) with {button}")

# Setting up the listener to monitor mouse events
with Listener(on_click=on_click) as listener:
    listener.join()