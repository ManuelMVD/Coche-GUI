from environment import *
class Light:
    def __init__(self,env):
        self.deactivate()
        self.env=env

    def activate(self):
        self.activated=True
 
    def deactivate(self):
        self.activated=False
 
    def update(self):
        if self.env.get_lum()<40:
            self.activate()
        else:
            self.deactivate()

    def __str__(self):
        if self.activated:
            status = 'L'
        else:
            status = ' '
        return status


