import tkinter as tk
from tkinter import ttk
import os
from tkinter import HORIZONTAL, Scale
from time import sleep
from blinker import *
from engine import *
from environment import *
from light import *
from fuel import *
from redlight import *

class Vehicle:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.canvas1=tk.Canvas(self.ventana1, width=665, height=285, background="black")
        self.canvas1.grid(column=0, row=0)
        archi1=tk.PhotoImage(file="1.png")
        self.img1 = self.canvas1.create_image(0,0, image=archi1, anchor="nw")
        archi2=tk.PhotoImage(file="2.png")
        self.img2 = self.canvas1.create_image(0,0, image=archi2, anchor="nw", state='hidden')

        self.state = 0 # dos estados según se muestre 1.png o 2.png
        self.count = 0 # para saber cuándo cambiar de estado

        self.blinker_front = Blinker(BLINKER_FRONT)
        self.blinker_front.start()
        self.blinker_front_polygon=self.canvas1.create_polygon(579,180,582,191,583,202,586,202,585,190,582,180, fill="orange", state='hidden')

        self.blinker_rear = Blinker(BLINKER_REAR)
        self.blinker_rear.start()
        self.blinker_rear_polygon=self.canvas1.create_polygon(42,176,42,179,46,181,53,181,52,178,50,177, fill="red", state='hidden')

        self.light_polygon=self.canvas1.create_polygon(584,146,664,146, 664,177,584,158,stipple="gray50", fill="yellow", state='hidden')
        self.light_rear_polygon=self.canvas1.create_polygon(50,144,85,135,86,127,49,129,stipple="gray50", fill="red", state='hidden')        

        self.redlight_polygon = [ self.canvas1.create_polygon(452,202,464,202,468,198,456,198,fill="red", state='hidden'), \
            self.canvas1.create_polygon(458,197,469,197,473,42,463,42,fill="red", state='hidden'), \
            self.canvas1.create_polygon(463,191,472,191,475,188,467,188,fill="red", state='hidden'), \
            self.canvas1.create_polygon(468,187,475,187,478,183,472,183,fill="red", state='hidden'), \
            self.canvas1.create_polygon(472,183,478,183,480,181,474,181,fill="red", state='hidden') ]

        self.engine = Engine()
        self.fuel = Fuel(self.engine)

        self.environment = Environment()
        self.light = Light(self.environment)
        
        self.redlight = RedLight()
        self.redlight.start()


        # añadir label para motor
        self.labelframe1=ttk.LabelFrame(self.ventana1, text="Engine:")        
        self.labelframe1.grid(column=0, row=10)    
        self.label1=ttk.Label(self.labelframe1, text=str(self.engine))
        self.label1.grid(column=0, row=10)
        
        # añadir para widget scale luminosidad
        self.labelframe2=ttk.LabelFrame(self.ventana1, text="Environment:")        
        self.labelframe2.grid(column=0, row=20, sticky = 'we')   
        self.label2 = tk.Label(self.labelframe2, text  = "[Valor escala]")
        self.label2.grid(column=0,row=0, sticky = 'we')

        self.scale = tk.Scale(self.labelframe2, from_ = 0, to = 99, orient = tk.HORIZONTAL, command=self.update_label, length = '665')
        self.scale.grid(column = 0, row = 0, sticky = 'we')
        self.scale.set(self.environment.get_lum())

    

        # añadir barra progreso combustible
        self.labelframe3 = ttk.LabelFrame(self.ventana1, text= 'Fuel')
        self.labelframe3.grid(column=0, row=30, sticky='we')
        self.progress = ttk.Progressbar(self.labelframe3, orient = HORIZONTAL, length= 665, mode='determinate')
        self.progress.pack(pady=10)
        self.progress['value'] = self.fuel.get_porcentage_level()





        self.ventana1.after(500,self.do_work) #se llama a la interfaz grafica cada cierto tiempo para actualizar datos.
        self.ventana1.bind("<KeyPress>", self.action)

        self.ventana1.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.ventana1.mainloop()
        

    def update_label(self, event):
        nueva_lum = self.scale.get()
        self.environment.set_lum(nueva_lum)


    def on_closing(self):
        self.ventana1.destroy()
        os._exit(1)

    def action(self,evento):
        if evento.keysym=='s':
                self.blinker_front.change()
        if evento.keysym=='a':
                self.blinker_rear.change()
        if evento.keysym=='r':
                self.environment.modify_lum(10)
                self.scale.set(self.environment.get_lum())
        if evento.keysym=='f':
                self.environment.modify_lum(-10)
                self.scale.set(self.environment.get_lum())
        if evento.keysym=='w':
                self.engine.modify_rpm(100)
        if evento.keysym=='z':
                self.engine.modify_rpm(-100)
        if evento.keysym == 'e':
                self.engine.modify_gear(1)
        if evento.keysym == 'd':
                self.engine.modify_gear(-1)        
        if evento.keysym=='c':
                self.redlight.activate()
        if evento.keysym=='v':
                self.redlight.deactivate()
        if evento.keysym=='g':
                self.fuel.reload()


    def draw_background(self):       
        
        colors = ["#020b0f","#05181f","#082530","#0b3141","#0e3e52","#197195","#1c7ea6", \
                    "#1e8bb7","#2197c7","#24a4d8"]
        lum = self.environment.get_lum()
        level = lum // 10

        self.canvas1.configure(background=colors[level])


    def draw_vehicle(self):

        porcentaje = abs(self.engine.get_speed()) / 100 # porcentaje de cada cuantas actualizaciones hay que cambiar de estado
                                                   # velocidad "maxima" es 100, porcentaje 1, siempre cambia de estado
        self.count = self.count + porcentaje
        if self.count >= 1: # ya podemos cambiar el estado
            self.count = 0
            self.state = self.state + 1
            if self.state > 1:
                self.state = 0

            if self.state == 0:
                self.canvas1.itemconfigure(self.img1, state='normal')
                self.canvas1.itemconfigure(self.img2, state='hidden')
            else:
                self.canvas1.itemconfigure(self.img1, state='hidden')
                self.canvas1.itemconfigure(self.img2, state='normal')


    def draw_blinker_front(self):
        if self.blinker_front.get_activated():
            self.canvas1.itemconfigure(self.blinker_front_polygon, state='normal')
        else:
            self.canvas1.itemconfigure(self.blinker_front_polygon, state='hidden')


    def draw_blinker_rear(self):
        if self.blinker_rear.get_activated():
            self.canvas1.itemconfigure(self.blinker_rear_polygon, state='normal')
        else:
            self.canvas1.itemconfigure(self.blinker_rear_polygon, state='hidden')


    def draw_light(self):              
        if self.light.activated:
            self.canvas1.itemconfigure(self.light_polygon, state='normal')
            self.canvas1.itemconfigure(self.light_rear_polygon, state='normal')            
        else:
            self.canvas1.itemconfigure(self.light_polygon, state='hidden')
            self.canvas1.itemconfigure(self.light_rear_polygon, state='hidden')                        


    def draw_redlight(self):               
        level = self.redlight.get_status()
        pos=1
        for l in self.redlight_polygon:
            if pos<=level:
                self.canvas1.itemconfigure(l, state='normal')
            else:
                self.canvas1.itemconfigure(l, state='hidden')                
            pos=pos+1
    

    def do_work(self): #Metodo para actualizar interfaz grafica.
        self.ventana1.after(10,self.do_work)

        self.light.update()
        self.fuel.update()
        self.progress['value'] = self.fuel.get_porcentage_level()
        if self.fuel.get_porcentage_level() <= 0:
            self.engine.stop()
        self.labelframe3.update_idletasks()  
        self.draw_background()

        if self.fuel.get_porcentage_level()>0:
            self.draw_vehicle()

        self.draw_blinker_front()
        self.draw_blinker_rear()
        self.draw_light()
        self.draw_redlight()
        self.label1.config(text=str(self.engine))

vehicle1 = Vehicle()
