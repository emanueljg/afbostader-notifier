@echo off

call venv\Scripts\activate.bat
call pyinstaller notifier.py ^
    --distpath notifier-program\notifier ^
    --icon notifier-program\notifier\building.ico ^
    --noconsole ^
    --hidden-import plyer.platforms.win.notification ^
    --onefile

copy config.yaml notifier-program\notifier\config.yaml /Y
