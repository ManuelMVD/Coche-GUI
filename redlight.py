import threading
from time import sleep

max_pos = 5

class RedLight(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.deactivate()
        self.i = 0

    def activate(self):
        self.activated=True

    def deactivate(self):
        self.pos=0  # number of lights on
        self.i = 0
        self.activated=False

    def get_activated(self):
        return self.activated

    def get_status(self):
        return self.pos

    def run(self):
        while True:
            while self.activated:
                self.pos = self.i % max_pos
                self.i += 1
                sleep(0.2)