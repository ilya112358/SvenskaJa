call env\scripts\activate.bat
pyinstaller --noconfirm myproj.py
pyinstaller --noconfirm fillbase.py
xcopy /e /y dist C:\Users\Public\Downloads\dist
pause