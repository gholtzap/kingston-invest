@echo off

IF "%CD%"=="C:\Users\Gavin\dev\Kingston\kingston-invest" GOTO runscripts
cd /d C:\Users\Gavin\dev\Kingston\kingston-invest

:runscripts
python generate_data.py
python data_to_pic.py
python collage.py
python wallpaper.py
python email_summary.py