import ctypes
import os
from quote import quote
import random

SPI_SETDESKWALLPAPER = 20

script_dir = os.path.dirname(os.path.abspath(__file__))
WALLPAPER_PATH = os.path.join(script_dir, "collage.jpg")

if os.path.isfile(WALLPAPER_PATH):
    res = quote('Lincoln')
    
    try:
        print(f"\nDaily Lincoln quote: {res[random.randint(0, len(res))]['quote']}\n")
    except IndexError:
        print("\nNo quotes from Abe Lincoln available today.\n")
        
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
    print("Wallpaper set!")
else:
    print("File not found: " + WALLPAPER_PATH)
