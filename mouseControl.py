import cv2
import time
from pynput.mouse import Button, Controller as MouseController

class Controller:
    def __init__(self):
        self.mouse = MouseController()

    def set_mouse_position(self,x,y):
            self.mouse.position = (int(x),int(y))

    def smooth_move_mouse(self,from_x,from_y,to_x,to_y,speed=1):
    #steps might be changed to match with application frame
        steps = 40
        sleep_per_step = speed // steps
        x_delta = (to_x - from_x) / steps
        y_delta = (to_y - from_y) / steps
        for step in range(steps):
            new_x = x_delta * (step + 1) + from_x
            new_y = y_delta * (step + 1) + from_y
            self.set_mouse_position(new_x, new_y)
            time.sleep(1/speed)

    def move_mouse(self,from_x,from_y,to_x,to_y,speed = 1):
        self.set_mouse_position(from_x,from_y);
        time.sleep(1/speed);
        self.set_mouse_position(to_x,to_x);


    def left_mouse_click(self):
        self.mouse.click(Button.left)

    def left_mouse_drag(self,start,end):
        steps = 5
        xd = (end[0] - start[0]) / steps
        yd = (end[1] - start[1]) / steps
        self.set_mouse_position(start[0],start[1])
        time.sleep(0.5)
        self.mouse.press(Button.left)
        for step in range(steps):
            x = xd * (step + 1) + start[0]
            y = yd * (step + 1) + start[1]
            self.set_mouse_position(x,y);
            time.sleep(0.1)
        self.mouse.release(Button.left)