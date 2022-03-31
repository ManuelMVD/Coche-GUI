import threading
from time import sleep

# Blinker position (pos attribute)
BLINKER_FRONT = 1
BLINKER_REAR = 2

class Blinker(threading.Thread):
    def __init__(self, pos):
        threading.Thread.__init__(self)

        self.pos=pos       

        self.blinking=False
        self.deactivate()

        self.go_blink = False

    def activate(self):
        self.activated=True

    def deactivate(self):
        self.activated=False

    def blink(self):
        self.blinking=not self.blinking
        if not self.blinking:
            self.deactivate()
        else:
            self.activate()


    def get_activated(self):
        return self.activated


    def change(self):
        self.activated = not self.activated
    
    def change_go_blink(self):
        self.go_blink = not self.go_blink
        if not self.go_blink:
            self.activated = False

    def __str__(self):
        if self.activated:
            status = 'A'
        else:
            status = 'D'
        return status


    def run(self):
        while True:
            if self.go_blink:        
                self.blink()  
            sleep(0.5)
