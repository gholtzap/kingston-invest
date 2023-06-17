import ctypes
import os

SPI_SETDESKWALLPAPER = 20
WALLPAPER_PATH = r"C:\Users\tibbe\stocks-test2\collage.jpg" 

if os.path.isfile(WALLPAPER_PATH):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
else:
    print("File not found: " + WALLPAPER_PATH)
