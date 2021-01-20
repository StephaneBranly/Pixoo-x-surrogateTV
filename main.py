import pixoo as p
import pixelArt as pa
import os
import time

def main():
    device = p.Pixoo()
    device.connect()
    user="branlyst"
    device.show_image(os.path.join(os.path.dirname(__file__),"./logo.png"))
    time.sleep(2) 
    # device.displayText("",(120,0,120),(232,9,110))
    pixelArtGame = pa.PixelArt(device,user)
    
main()
