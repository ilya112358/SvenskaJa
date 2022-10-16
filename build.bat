call env\scripts\activate.bat
pyinstaller --noconfirm practice.py
pyinstaller --noconfirm fillbase.py
cd executable
del /q *.*
xcopy ..\dist\fillbase
xcopy ..\dist\practice\practice.exe
xcopy ..\config.ini
xcopy ..\wordbase.txt
"c:\Program Files\WinRAR\WinRAR" a SvenskaJaWin.zip *.*
cd ..
pause
