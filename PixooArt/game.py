import argparse
import logging

import pixoo as p
from PIL import Image
import os
from datetime import datetime
import time

from surrortg.inputs import Joystick, Directions
from surrortg.inputs import Switch
from surrortg import Game

class GameJoystick(Joystick):
    def __init__(self, game, jid):
        self.game = game
        self.jid = jid
        
    async def handle_coordinates(self, x, y, seat=0):
        direction = self.get_direction_8(x, y)
        self.game.on_press(direction,self.jid)
  
class GameButton(Switch):
    def __init__(self, game, name):
        self.game = game
        self.name = name
        
    async def on(self, seat=0):
        self.game.on_press(self.name,0,1)

    async def off(self, seat=0):
        self.game.on_press(self.name,0,0)
       
class PixooArtGame(Game):
    def __init__(self,user="NaN"):
        self.image = Image.new('RGBA', (16, 16), color = 'black')
        self.image.save('./pixelArts/svg.png')
        self.screen=None
        self.cursorx=8
        self.cursory=8
        self.showCursor=True
        self.user = user
        self.clear = 0
        self.current = 1
        self.device = p.Pixoo()
        self.device.connect()
        self.colors = [(0,0,0),(255,255,255),(255,0,0),(255,127,0),(255,255,0),(127,255,0),(0,255,0),(0,255,127),(0,255,255),(0,127,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127)]
        
    async def on_init(self):
        logging.info("Init game")
        self.image = Image.new('RGBA', (16, 16), color = 'black')
        self.image.save('./pixelArts/svg.png')
        self.generateImage()
        self.screen=None
        self.cursorx=8
        self.cursory=8
        self.showCursor=True
        self.current = 1
        self.ready_for_next_game = True
        
        self.joystick_main = GameJoystick(self,1)
        self.joystick_colors = GameJoystick(self,2)
        self.io.register_inputs(
            {"joystick_main": self.joystick_main,
            "joystick_colors": self.joystick_colors,
            "quit_button": GameButton(self,"quit_button"),
            "clear_board": GameButton(self,"clear_board"),}
        )

        
        
    async def on_pre_game(self):
        logging.info("### On pre game ###")
        if self.user != self.players[0]['username']: 
            self.image = Image.new('RGBA', (16, 16), color = 'black')
            self.image.save('./pixelArts/svg.png')
            self.setUser(self.players[0]['username'])
        self.generateImage()
        self.screen=None
        self.cursorx=8
        self.cursory=8
        self.showCursor=True
        self.current = 1
        self.clear = 0
        self.colors = [(0,0,0),(255,255,255),(255,0,0),(255,127,0),(255,255,0),(127,255,0),(0,255,0),(0,255,127),(0,255,255),(0,127,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127)]
        self.io.send_pre_game_ready()
        
    async def on_start(self):
        self.ready_for_next_game = False
        logging.info("### Playing started ###")
        logging.info("  >   "+self.user+" is playing")
        self.device.show_image(os.path.join(os.path.dirname(__file__),"./logo.png"))
        time.sleep(3) 
        self.generateImage()
        self.io.enable_inputs()
        self.clear = 0
    
    async def on_finish(self):
        self.io.send_score(1)
        self.io.disable_inputs()
        self.ready_for_next_game = True
        logging.info("### Playing finished ###")
        now = datetime.now() 
        date_time = now.strftime("_%Y%m%d_%Hh%Mm%Ss")
        filename = (self.user)+date_time+".png"
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./pixelArts/svg.png"))
        logging.info("Image saved")
        self.image.save("pixelArts/"+filename)

    def setUser(self, user="Nan"):
        self.user = user
        
    def generateImage(self):
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./pixelArts/svg.png"))
        if(self.showCursor%2):
                self.addCursor()
        self.image.save('current.png')
        if self.clear:
                self.displayImage(im = os.path.join(os.path.dirname(__file__),"./pixelArts/clearBoard.png"))
        else:
                self.displayImage(im = os.path.join(os.path.dirname(__file__),"current.png"))
        
    def addPixelColor(self,rgb):
        self.image = Image.open(os.path.join(os.path.dirname(__file__),"./pixelArts/svg.png"))
        self.image.putpixel((self.cursorx,self.cursory), rgb)
        self.image.save('./pixelArts/svg.png')
        
    def addCursor(self):
        positions = [[-1,-1],[-1,1],[1,1],[1,-1]]
        for position in positions:
                if self.cursorx + position[0] >= 0 and self.cursorx + position[0]  < 16:
                        if self.cursory + position[1] >= 0 and self.cursory + position[1] < 16:
                                self.image.putpixel((self.cursorx + position[0],self.cursory+  position[1]), self.colors[self.current])
       
    def displayImage(self,im):
        self.device.show_image(im)
        
    def on_press(self, button, input_id, pressed=1):
        if input_id:
            self.clear = 0
        if input_id == 1: 
            if button == Directions.LEFT:
                self.cursorx=(self.cursorx-1)%16
            elif button == Directions.RIGHT:
                self.cursorx=(self.cursorx+1)%16
            elif button == Directions.TOP:
                self.cursory=(self.cursory-1)%16
            elif button == Directions.BOTTOM:
                self.cursory=(self.cursory+1)%16
        elif input_id == 2:
            if button == Directions.LEFT:
                self.current = (self.current - 1) % len(self.colors)
            elif button == Directions.RIGHT:
                self.current = (self.current + 1) % len(self.colors)
            elif button == Directions.TOP:
                self.addPixelColor(self.colors[self.current])
            elif button == Directions.BOTTOM:
                self.showCursor=self.showCursor+1  
                 
        elif button == "quit_button":
            self.io.send_playing_ended()
        elif button == "clear_board":
            if self.clear == 1 and pressed == 0:
                self.clear = self.clear + 1
            elif (self.clear == 0 and pressed == 1) or (self.clear == 2 and pressed == 1):
                self.clear = self.clear + 1
            if self.clear == 3:
                self.image = Image.new('RGBA', (16, 16), color = self.colors[self.current])
                self.image.save('./pixelArts/svg.png')
                self.clear = 0
        self.generateImage()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Pixoo Art Game")
    parser.add_argument(
        "-c",
        "--conf",
        metavar="",
        help="./config.toml",
        required=False,
    )
    args = parser.parse_args()
    if args.conf is not None:
        PixooArtGame().run("./config.toml")
        logging.info("Run with args")
    else:
        PixooArtGame().run()
        logging.info("Run without args")
