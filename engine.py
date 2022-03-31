
class Engine:
    def __init__(self):
        self.rpm=0
        self.gear=0
        
    def modify_rpm(self,variation):
        self.rpm = self.rpm+variation
        if self.rpm<0:
            self.rpm=0

    def modify_gear(self,variation):
        self.gear = self.gear+variation
        if self.gear<-1:
            self.gear=-1
        elif self.gear>5:
            self.gear=5

    def get_speed(self):        
        if self.gear>=0:
            res = (self.rpm*self.gear/5)/10
        elif self.rpm>0:
            res = -10
        else:
            res = 0
            
        return res

    def stop(self):
        self.rpm = 0

    def __str__(self):
        status = str(self.rpm) +" rpm " +str(self.gear)+" "+str(self.get_speed()) + " km/h"
        return status

