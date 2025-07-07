# -*- coding: utf-8 -*-
"""
@author: jonas.stephan
"""

from pynput.mouse import Listener, Button   
import mss
import mss.tools
import sys
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtWidgets, QtCore
from pynput import mouse


'''globals'''
# path = os.getcwd()
path = sys.path[0]
ui_path = os.path.join(path, 'qt\\colordetection.ui')
config_path = os.path.join(path, 'config.json')
logo_path = os.path.join(path, 'qt\\logo.png')
stylesheet_path = os.path.join(path, 'qt\\Toolery.qss')


class Ui(QtWidgets.QDialog):
    color_detected = pyqtSignal(int, int, int)

    def __init__(self):
        super(Ui, self).__init__()

        # UI laden
        uic.loadUi(ui_path, self)
        self.setFixedWidth(300)
        self.setFixedHeight(235)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.show()

        print("\nColor detection by JS\nRight-click anywhere on the screen to start color recognition!")

        # Buttons
        self.exitButton = self.button_exit
        self.exitButton.clicked.connect(self.close)

        self.infoButton = self.button_info
        self.infoButton.clicked.connect(self.info)

        # Labels
        self.colorLabel = self.label_color
        self.colorLabel.setText('')
        self.rLabel = self.label_r
        self.gLabel = self.label_g
        self.bLabel = self.label_b
        self.hexLabel = self.label_hex

        # Edits    
        self.rEdit = self.edit_r
        self.gEdit = self.edit_g
        self.bEdit = self.edit_b
        self.hexEdit = self.edit_hex

        # color detection signal
        self.color_detected.connect(self.update_color_display)

        # start right click listener
        self.global_click_listener = mouse.Listener(on_click=self.global_on_click)
        self.global_click_listener.start()

        self.listener = None

    def global_on_click(self, x, y, button, pressed):
        if pressed:
            # check for right mouse button
            if button == Button.right:
                print("Start color detection")
                self.detect()

    def detect(self):
        if self.listener is not None and self.listener.running:
            print("Color detection is already running!")
            return

        # start pixel listener
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()

    def info(self):
        QtWidgets.QMessageBox.information(
            self,
            "Info",
            "Right-click anywhere on the screen to start color recognition!\nLeft-click reads the color, middle-click ends color recognition."
        )

    def rgb2hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def get_pixel_color(self, x, y):
        with mss.mss() as sct:
            bbox = {'top': y, 'left': x, 'width': 1, 'height': 1}
            img = sct.grab(bbox)
            color = img.pixel(0, 0)
            return (color[2], color[1], color[0])

    def on_click(self, x, y, button, pressed):
        if pressed:
            # check for left mouse click
            if button == Button.left:
                b, g, r = self.get_pixel_color(x, y)
                print(f'Color detected ({r}, {g} {b})')
                self.color_detected.emit(r, g, b)

            # middle mouse button
            if button == Button.middle:
                print("Stop color detection")
                if self.listener is not None:
                    self.listener.stop()

    def update_color_display(self, r, g, b):
        val_hex = self.rgb2hex(r, g, b)

        self.rEdit.setText(str(r))
        self.gEdit.setText(str(g))
        self.bEdit.setText(str(b))
        self.hexEdit.setText(str(val_hex).upper())

        self.update_label_color(r, g, b)

    def update_label_color(self, r, g, b):
        style = f"background-color: rgb({r}, {g}, {b});"
        self.colorLabel.setStyleSheet(style)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    with open(stylesheet_path, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    window = Ui()
    app.exec_()



            
