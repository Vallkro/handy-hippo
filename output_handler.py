from pynput.mouse import Button, Controller
import numpy as np
class OutputHandler():

    def __init__(self):
        self.name = "Output handler"
        self.previous_coords = None
        self.tol = 0.005
        self.mouse = Controller()
        self.step_size = 2
        self.P = 1000
    def indexscroll(self, coords):
    
        if self.previous_coords is not None:
            # y coords inverterded
            y_diff = coords.y - self.previous_coords.y
            if y_diff - self.tol > 0 :
                print("Scrolling up ")
                self.mouse.scroll(0,self.step_size)
            elif y_diff + self.tol < 0 :
                print("Scrolling down ")
                self.mouse.scroll(0,-self.step_size)

        #Save last coords
        self.previous_coords = coords
    
    def mouse_control(self, index_coords, thumb_coords):
        # Filter theese coords!
        x_dist_th_index_sq = (index_coords.x - thumb_coords.x)**2
        y_dist_th_index_sq = (index_coords.y - thumb_coords.y)**2
        distance_thumb_index_sq = x_dist_th_index_sq + y_dist_th_index_sq

        if distance_thumb_index_sq < self.tol and self.previous_coords is not None:
            print("Thumb and index finger closed, moving mouse")
            y_diff = index_coords.y - self.previous_coords.y
            x_diff = index_coords.x - self.previous_coords.x
            self.mouse.move(x_diff*self.P, y_diff*self.P)
        
        self.previous_coords = index_coords


        

