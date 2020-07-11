call venv\Scripts\activate.bat
call pyinstaller notifier.py --distpath notifier-program\notifier --noconsole --hidden-import plyer.platforms.win.notification --onefile
copy config.yaml notifier-program\notifier\config.yaml /Y
