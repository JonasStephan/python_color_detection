# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:01:27 2025

@author: jonas.stephan
"""

import pyautogui
from PIL import ImageGrab
import time

def get_pixel_color(x, y):
    # Screenshot vom Bildschirm (schnell)
    image = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    color = image.getpixel((0, 0))
    return color

try:
    print("Bewege die Maus über eine Stelle, um den Pixel-Farbwert zu sehen. Drücke STRG+C zum Beenden.\n")
    time.sleep(1)
    while True:
        # if pyautogui.click():  # click the mouse
            x, y = pyautogui.position()
            color = get_pixel_color(x, y)
            print(f"Position: ({x}, {y}) | Farbe (RGB): {color}", end='\r')
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBeendet.")