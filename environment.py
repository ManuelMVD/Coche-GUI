
class Environment:
    def __init__(self):
        self.lum = 50 # 0-100%

    def modify_lum(self,variation):
        self.lum = self.lum+variation
        if self.lum<0:
            self.lum=0
        elif self.lum>=99:
            self.lum=99

    def set_lum(self,lum):
        self.lum=lum


    def get_lum(self):
        return self.lum
