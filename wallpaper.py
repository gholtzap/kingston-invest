import ctypes
import os
from quote import quote
import random

SPI_SETDESKWALLPAPER = 20
WALLPAPER_PATH = r"C:\Users\tibbe\stocks-test2\collage.jpg" 

if os.path.isfile(WALLPAPER_PATH):
    res = quote('DaVinci')
    print(f"\nDaily DaVinci quote: {res[random.randint(0, len(res))]['quote']}\n")
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
    print("Wallpaper set!")
else:
    print("File not found: " + WALLPAPER_PATH)
