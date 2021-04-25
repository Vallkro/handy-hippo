from pynput.mouse import Button, Controller

class OutputHandler():

    def __init__(self):
        self.name = "Output handler"
        self.previous_coords = None
        self.tol = 0.1
        self.mouse = Controller()
        self.step_size = 2
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

