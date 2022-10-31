call env\scripts\activate.bat
pyinstaller --noconfirm maintain.py
pyinstaller --noconfirm practice.py
cd executable
del /q *.*
xcopy ..\dist\maintain
xcopy ..\dist\practice\practice.exe
xcopy ..\wordbase.txt
"c:\Program Files\WinRAR\WinRAR" a SvenskaJaWin.zip *.*
cd ..
pause
