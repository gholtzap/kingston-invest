import ctypes
import os
import winreg
import logging
import coloredlogs

# Set up logging with coloredlogs
coloredlogs.install(level='INFO')
logging.basicConfig(level=logging.INFO)

SPI_SETDESKWALLPAPER = 20

script_dir = os.path.dirname(os.path.abspath(__file__))
WALLPAPER_PATH = os.path.join(script_dir, "collage.png")

if os.path.isfile(WALLPAPER_PATH):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
    tile_wallpaper = "0"
    wallpaper_style = "2"
    winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, tile_wallpaper)
    winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, wallpaper_style)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
    logging.info("Wallpaper set!")
else:
    logging.error("File not found: " + WALLPAPER_PATH)
