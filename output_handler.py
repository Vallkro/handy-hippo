from pynput.mouse import Button, Controller
import numpy as np

class RollingAvg:

    def __init__(self, steps = 10, states = 3) :
        from collections import deque
        self.steps = steps
        self.past_values = None
        self.state_size = states

    def get_avg(self):
        if self.past_values is not None:
            rolling_avg = np.sum(self.past_values, axis = 1, keepdims = True)
            #rolling_avg = np.sum(self.past_values)/self.steps
            return rolling_avg/self.steps
        else:
            return None

    def update(self, x):
        if self.past_values is None :
            #self.past_values = np.full((self.state_size, self.steps),x)
            self.past_values = np.broadcast_to(x,(len(x),self.steps))
        else:
            self.past_values = np.column_stack([self.past_values,x])[:,1:]

class OutputHandler():

    def __init__(self):
        self.name = "Output handler"
        self.previous_coords = None
        self.tol = 0.002
        self.tol_upper = 0.01
        self.tol_lower = 0.003
        self.mouse = Controller()
        self.step_size = 2
        self.P = 1000
        self.ra = RollingAvg(steps = 5, states = 9)
        self.button_left_down = False
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
    
    def mouse_control(self, index_coords, thumb_coords, middle_finger_coords):
        # Filter theese coords!
        thumb_list = np.array([thumb_coords.x, thumb_coords.y, thumb_coords.z])
        index_list = np.array([index_coords.x, index_coords.y, index_coords.z])
        middle_finger_list = np.array([middle_finger_coords.x, middle_finger_coords.y, middle_finger_coords.z])
        prev_state = self.ra.get_avg()
        new_state = np.append(np.append(index_list,thumb_list),middle_finger_list)
        new_state.shape = (len(new_state),1) # make sure its a vector 
        self.ra.update(new_state)
        state = self.ra.get_avg()
        # calc distances between fingertips
        x_dist_th_index_sq = (state[0] - state[3])**2
        y_dist_th_index_sq = (state[1] - state[4])**2
        distance_thumb_index_sq = x_dist_th_index_sq + y_dist_th_index_sq

        x_dist_index_middle_sq = (state[3] - state[6])**2
        y_dist_index_middle_sq = (state[4] - state[7])**2
        distance_index_middle_sq = x_dist_index_middle_sq + y_dist_index_middle_sq
        #print(state)
        if distance_index_middle_sq < self.tol_lower and not self.button_left_down:
            print("Index and middle closed, pressing left button")
            self.mouse.press(Button.left)
            self.button_left_down = True
        elif distance_index_middle_sq > self.tol_upper and self.button_left_down:
            print("Index and middle open, releasing left button")
            self.mouse.release(Button.left)
            self.button_left_down = False

        if distance_thumb_index_sq < self.tol and prev_state is not None:
            #y_diff = index_coords.y - self.previous_coords.y
            #x_diff = index_coords.x - self.previous_coords.x
            x_diff = state[3] - prev_state[3]
            y_diff = state[4] - prev_state[4]
            self.mouse.move(x_diff*self.P, y_diff*self.P)
            print(f"Thumb and index finger closed, moving mouse ( {x_diff*self.P}, {y_diff*self.P}) ")
        

if __name__ == "__main__":
   ra = RollingAvg(10,3)
   a = np.array([1,2,3])
   ra.update(a)
   print(ra.past_values)
   print(ra.get_avg())



        

