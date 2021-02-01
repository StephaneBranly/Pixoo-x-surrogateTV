import pixoo as p
import pixelArt as pa
import os
import time

def main():
    device = p.Pixoo()
    device.connect()
    pixelArtGame = pa.PixelArt(device)

    while 1:
        device.reconnect()
        pixelArtGame.setUser("branlyst")
        # device.show_image(os.path.join(os.path.dirname(__file__),"./logo.png"))
        # time.sleep(3) 
        pixelArtGame.reset("branlyst")
        pixelArtGame.run()
    
main()
