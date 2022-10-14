call env\scripts\activate.bat
pyinstaller --noconfirm practice.py
pyinstaller --noconfirm fillbase.py
xcopy /e /y dist\fillbase executable
xcopy /e /y dist\practice executable
pause