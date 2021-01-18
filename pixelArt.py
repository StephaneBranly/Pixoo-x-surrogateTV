from PIL import Image
from pynput import keyboard
import os
from datetime import datetime

class PixelArt:
    def __init__(self,display,user):
        self.image = Image.new('RGBA', (16, 16), color = 'black')
        self.image.save('svg.png')
        self.cursorx=8
        self.cursory=8
        self.showCursor=True
        self.display=display
        self.generateImage()
        self.loop = True
        self.user = user
        self.run()

    def closeGame(self):
        now = datetime.now() 
        date_time = now.strftime("_%Y%m%d_%H-%M-%S")
        filename = (self.user)+date_time+".png"
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"svg.png"))
        self.image.save("pixelArts/"+filename)

    def on_press(self,key):
        if key == keyboard.Key.left:
            self.cursorx=(self.cursorx-1)%16
        elif key == keyboard.Key.right:
            self.cursorx=(self.cursorx+1)%16
        elif key == keyboard.Key.up:
            self.cursory=(self.cursory-1)%16
        elif key == keyboard.Key.down:
            self.cursory=(self.cursory+1)%16
        elif 'char' in dir(key):
            if key.char == 'q':    #check if it is 'q' key
                self.loop=False
                keyboard.Listener.stop
                self.closeGame()
            elif key.char == 'y':
                self.addPixelColor(255,255,0) 
            elif key.char == 'e':
                self.addPixelColor(0,0,0)
            elif key.char == 'w':
                self.addPixelColor(255,255,255) 
            elif key.char == 'o':
                self.addPixelColor(255,165,0) 
            elif key.char == 'b':
                self.addPixelColor(0,0,255) 
            elif key.char == 'c':
                self.addPixelColor(0,255,255)
            elif key.char == 'g':
                self.addPixelColor(0,255,0)
            elif key.char == 'r':
                self.addPixelColor(255,0,0)  
            elif key.char == 'm':
                self.addPixelColor(255,0,255)
            elif key.char == 'p':
                self.addPixelColor(128,0,128)  
            elif key.char == 'h':
                self.showCursor=self.showCursor+1
      
        self.generateImage()

    def run(self):
        while self.loop:
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
            
    def addPixelColor(self,r,g,b):
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./svg.png"))
        self.image.putpixel((self.cursorx,self.cursory), (r, g, b))
        self.image.save('svg.png')

    def generateImage(self):
        # self.image.putpixel((self.cursorx,self.cursory), (255, 0, 0))
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./svg.png"))
        if(self.showCursor%2):
            self.addCursor()
        self.image.save('current.png')
        self.displayImage(im = os.path.join(os.path.dirname(__file__),"./current.png"))
    
    def addCursor(self):
        if(self.cursorx>1):
            for i in range(0,self.cursorx-1):
                self.image.putpixel((i,self.cursory), (255, 0, 0))
        if(self.cursorx<15):
            for i in range(self.cursorx+2,16):
                self.image.putpixel((i,self.cursory), (0, 255, 255))
        if(self.cursory>1):
            for i in range(0,self.cursory-1):
                self.image.putpixel((self.cursorx,i), (0, 0, 255))
        if(self.cursory<15):
            for i in range(self.cursory+2,16):
                self.image.putpixel((self.cursorx,i), (255, 255, 0))

    def displayImage(self,im):
        self.display.show_image(im)

