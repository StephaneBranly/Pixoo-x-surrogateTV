from PIL import Image
import pygame
import os
from datetime import datetime

class PixelArt:
    def __init__(self,display,user="NaN"):
        self.image = Image.new('RGBA', (16, 16), color = 'black')
        self.image.save('svg.png')
        self.cursorx=8
        self.cursory=8
        self.showCursor=True
        self.display=display
        self.user = user
        
    def setUser(self, user="Nan"):
        self.user = user

    def closeGame(self):
        now = datetime.now() 
        date_time = now.strftime("_%Y%m%d_%Hh%Mm%Ss")
        filename = (self.user)+date_time+".png"
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"svg.png"))
        self.image.save("pixelArts/"+filename)

    def reset(self, user="Nan"):
        if(user!=self.user):
            self.image = Image.new('RGBA', (16, 16), color = 'black')
            self.image.save('svg.png')
        self.generateImage()

    def on_press(self,key):
        if key == pygame.K_LEFT:
            self.cursorx=(self.cursorx-1)%16
        elif key == pygame.K_RIGHT:
            self.cursorx=(self.cursorx+1)%16
        elif key == pygame.K_UP:
            self.cursory=(self.cursory-1)%16
        elif key == pygame.K_DOWN:
            self.cursory=(self.cursory+1)%16
        elif key == pygame.K_q:    #check if it is 'q' key
            self.loop=False
            self.closeGame()
        elif key == pygame.K_y:
            self.addPixelColor(255,255,0) 
        elif key == pygame.K_e:
            self.addPixelColor(0,0,0)
        elif key == pygame.K_w:
            self.addPixelColor(255,255,255) 
        elif key == pygame.K_o:
            self.addPixelColor(255,165,0) 
        elif key == pygame.K_b:
            self.addPixelColor(0,0,255) 
        elif key == pygame.K_c:
            self.addPixelColor(0,255,255)
        elif key == pygame.K_g:
            self.addPixelColor(0,255,0)
        elif key == pygame.K_r:
            self.addPixelColor(255,0,0)  
        elif key == pygame.K_m:
            self.addPixelColor(255,0,255)
        elif key == pygame.K_p:
            self.addPixelColor(128,0,128)  
        elif key ==  pygame.K_h:
            self.showCursor=self.showCursor+1
      
        self.generateImage()

    def run(self):
        self.loop = True
        pygame.init()
        pygame.display.set_mode((16, 16))
        pygame.display.set_caption("pixelArtGame")
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.on_press(event.key)
            
    def addPixelColor(self,r,g,b):
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./svg.png"))
        self.image.putpixel((self.cursorx,self.cursory), (r, g, b))
        self.image.save('svg.png')

    def generateImage(self):
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./svg.png"))
        if(self.showCursor%2):
            self.addCursor()
        self.image.save('current.png')
        self.displayImage(im = os.path.join(os.path.dirname(__file__),"./current.png"))
    
    def addCursor(self):
        positions = [[-2,-1],[-1,-2],[-2,1],[-1,2],[2,-1],[1,-2],[2,1],[1,2]]
        for position in positions:
            if self.cursorx + position[0] >= 0 and self.cursorx + position[0]  < 16:
                if self.cursory + position[1] >= 0 and self.cursory + position[1] < 16:
                     self.image.putpixel((self.cursorx + position[0],self.cursory+  position[1]), (255, 0, 0))
       
    def displayImage(self,im):
        self.display.show_image(im)

