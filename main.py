import pixoo as p
import pixelArt as pa
import os

def main():
    device = p.Pixoo()
    device.connect()
    device.show_scoreboard(1,2)
    pixelArtGame = pa.PixelArt(device,"branlyst")
    
main()
