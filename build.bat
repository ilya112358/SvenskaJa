call env\scripts\activate.bat
pyinstaller --noconfirm practice.py
pyinstaller --noconfirm fillbase.py
xcopy /e /y dist\fillbase C:\Users\Public\Downloads\SvenskaJa
xcopy /e /y dist\practice C:\Users\Public\Downloads\SvenskaJa
pause